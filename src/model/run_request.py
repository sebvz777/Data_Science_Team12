import os
import re
from azure.ai.language.questionanswering import QuestionAnsweringClient
from azure.core.credentials import AzureKeyCredential
from elasticsearch import Elasticsearch
from azure.ai.language.questionanswering import models as qna

# Azure Cognitive Services credentials
azure_endpoint = "https://dsproject.cognitiveservices.azure.com/"
azure_api_key = "1041c8be86c14b9ebe6dcfe758c875f9"

project_name = "DataScienceProject"
deployment_name = "test"

# Elasticsearch setup
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

# Initialize the Azure Question Answering client
qa_client = QuestionAnsweringClient(azure_endpoint, AzureKeyCredential(azure_api_key))

def text_to_sentence_list(text):
    # Remove newline characters and extra spaces
    cleaned_text = text.replace('\n', ' ').strip()
    
    # Use regex to split the text into sentences
    # This regex handles common sentence-ending punctuation marks followed by spaces
    sentence_list = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!|\n)\s', cleaned_text)
    
    return sentence_list

def search_elasticsearch(query):
    # Query Elasticsearch
    response = es.search(
        index="test11",
        body={
            "query": {
                "match": {
                    "attachment.content": query
                }
            },
            "size": 10000  # Adjust this to retrieve a large number of documents if needed
        }
    )
    return response


# returns two strings
def get_best_answer(question):
    print("Get Answer started \n")
    # Search Elasticsearch for relevant documents
    es_response = search_elasticsearch(question)
    
    # Extract the relevant text from the Elasticsearch response
    hits = es_response['hits']['hits']
    all_hits = []
    all_hits_content = []
    
    for hit in hits:
        content = hit['_source']['attachment']['content']
        source = hit['_source']['filename']

        sentences = text_to_sentence_list(content)
        all_hits_content.extend(sentences)
        all_hits.extend([(sentence, source) for sentence in sentences])

    if not all_hits_content:
        return "No Documents regarding that Question found.", "src: none"

    best_answer = None
    highest_confidence = 0
    
    print("Starting the querries \n")
    # Process sentences in batches of 5
    for i in range(0, len(all_hits_content), 5):
        batch = all_hits_content[i:i+5]
        
        input = qna.AnswersFromTextOptions(
            question=question,
            text_documents=batch
        )

        print("getting output for batch: \n")
        for hits in batch:
            print(hits + "\n")
        output = qa_client.get_answers_from_text(input, language="de")
        print("batch completed \n")

        # Find the best answer from this batch
        for answer in output.answers:
            print("getting stuck on answer extraction")
            if answer.confidence > highest_confidence:
                highest_confidence = answer.confidence
                best_answer = answer

    print("getting here")
    # Print the best answer and its source
    if best_answer and highest_confidence > 0:
        print(u"Question: {}".format(question))
        print(u"Answer: {}".format(best_answer.answer))
        print(u"Confidence: {}".format(best_answer.confidence))
        for (content, source) in all_hits:
            if best_answer.answer in content:
                print(u"Source: {}".format(source))
                return best_answer.answer, source
    else:
        return "No answer with high enough confidence found.", "src: none"

if __name__ == "__main__":
    #print(search_elasticsearch(query="Ansprechpartner"))
    #question = input("Ask a question: ")
    print(get_best_answer("Wie oft wird die Risikoanalsye durchgeführt?"))
