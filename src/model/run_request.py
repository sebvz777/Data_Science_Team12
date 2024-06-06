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
        index="test5",
        body={
            "query": {
                "match": {
                    "attachment.content": query
                }
            }
        }
    )
    return response

def get_best_answer(question):
    # Search Elasticsearch for relevant documents
    es_response = search_elasticsearch(question)
    
    # Extract the relevant text from the Elasticsearch response
    hits = es_response['hits']['hits']
    # Extracting the content from the hits
    all_hits = []
    all_hits_content = []
    for hit in hits:
        content = hit['_source']['attachment']['content']
        source = hit['_source']['filename']

        sentences = text_to_sentence_list(content)
        for sentence in sentences:
            all_hits_content.append(sentence)
            all_hits.append((sentence, source))

        

    input = qna.AnswersFromTextOptions(
        question=question,
        text_documents=all_hits_content
    )

    if (all_hits):
        output = qa_client.get_answers_from_text(input, language="de")
    
        # Print all answers
        #for answer in output.answers:
        #    print(f"Answer: {answer.answer}, Confidence: {answer.confidence}")

        best_answer = [a for a in output.answers if a.confidence > 0][0]
        print(u"Question: {}".format(question))
        print(u"Answer: {}".format(best_answer.answer))
        for (content, source) in all_hits:
            if best_answer.answer in content:
                print(u"Source: {}".format(source))

    return best_answer.answer, source

if __name__ == "__main__":
    #print(search_elasticsearch(query="Ansprechpartner"))
    #question = input("Ask a question: ")
    answer, source  = get_best_answer("Wer ist der Ansprechpartner?")