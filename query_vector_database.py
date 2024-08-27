import argparse
from get_embedding_function import get_embedding_function
from langchain.vectorstores.chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama

PROMPT_TEMPLATE = """
    Answer the question based only on the following context:
    {context}
    - -
    Answer the question based on the above context: {question}
    """

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", type=str, help="Prompt to ask LLM")
    parser.add_argument("--embedding_function", default="OllamaEmbeddings", type=str, help="Select The Embedding Function")
    parser.add_argument("--chroma_db_name", default="chroma", type=str, help="chroma database name to use")
    args = parser.parse_args()

    query_text = args.prompt 
    embedding_function = args.embedding_function
    chroma_path = args.chroma_db_name

    formatted_response, response_text = query_rag(query_text, embedding_function, chroma_path)
    print(formatted_response)

def query_rag(query_text, embedding, chroma_path):
    """
    Query a Retrieval-Augmented Generation (RAG) system using Chroma database and Ollama mistral.
    Args:
    - query_text (str): The text to query the RAG system with, based off of the prompt given to LLM.
    - embedding (str): The embedding function used when initializing the vector-database.
    - chroma_path (str): chroma database name that was assigned to it.
    Returns:
    - formatted_response (str): Formatted response including the generated text and sources.
    - response_text (str): The generated response text.
    """

    embedding_func = get_embedding_function(embedding)

    db = Chroma(persist_directory=chroma_path, embedding_function=embedding_func)

    #Ensure that the database is called correctly
    print("Number of chunks in the database:", len(db))

    #Retrieving the context from the DB using similarity search
    results = db.similarity_search_with_relevance_scores(query_text, k=3)

    # Combine context from matching documents
    context_text = "\n\n - -\n\n".join([doc.page_content for doc, _score in results])

    # Create prompt template using context and query text
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    
    #Initialize model from Ollama
    model = Ollama(model="mistral")

    #Prompt the model
    response_text = model.invoke(prompt)
    
    #Get sources of the matching documents
    sources = [doc.metadata.get("id", None) for doc, _score in results]
    
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    return formatted_response, response_text

if __name__ == "__main__":
    main()