# ---------------------------------------------------------------------------- #
# Inference Chain for Information Extraction
# 
# This module sets up a Retrieval-Augmented Generation (RAG) pipeline using
# OpenAI's GPT model to extract structured information from text documents.
# ---------------------------------------------------------------------------- #

from langchain.chains import RetrievalQA  # RAG pipeline for question answering
from langchain.prompts import PromptTemplate  # Template for structuring prompts
from langchain_community.chat_models import ChatOpenAI  # OpenAI chat model interface

# Define the prompt template for the main question-answering task
prompt_template = PromptTemplate(
    input_variables=["context"],
    template="""Answer ONLY using the context below, which includes document metadata:
        Context: {context}

        Question: Use the corpus of text provided below to extract the following information in a structured format:
        1. Dates on which military forces were killed in combat. You may use the published date and day of the week to determine the date.
        2a. An approximate range of the number of deaths (if precise figures are not available).
        2b. A precise figure for the number of deaths (if available).
        3. A list of two or more countries involved in the conflict. You may use the country codes to determine the countries involved.

        Format your response as follows:
        - Date: [Approximate range or YYYY-MM-DD]
        - Death Count: [Approximate range or precise figure]
        - Countries involved: [List of all countries involved]

        Include all possible answers from the context. Answer (based solely on the context provided, no explanations):
        """
)

# Define the prompt template for individual document formatting
document_prompt = PromptTemplate(
    input_variables=["page_content", "published_date", "country_codes"],
    template="""
    Article published date and day of the week: {published_date}, 
    Countries involved:{country_codes}
    Content: {page_content}
    """
)

def ask_gpt(vector_store):
    """
    Set up and execute a RAG pipeline to query a vector store using GPT.
    
    Args:
        vector_store: The vector store containing document embeddings.
        
    Returns:
        dict: The response from the GPT model, including source documents.
    """
    # Initialize the OpenAI language model with specific parameters
    llm = ChatOpenAI(model="gpt-4", temperature=0)

    # Configure the retriever to fetch relevant documents based on similarity
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 10}  # Retrieve top 10 similar documents
    )
    
    # Set up the RAG pipeline with the language model and retriever
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        return_source_documents=True,
        chain_type_kwargs={
            "prompt": prompt_template,
            "document_prompt": document_prompt
        }
    )

    # Define the query to be asked
    query = "Find dates and death counts related to military forces killed in combat."
    # Execute the query and return the response with source documents
    response_with_sources = qa_chain({"query": query}, return_only_outputs=False)

    return response_with_sources