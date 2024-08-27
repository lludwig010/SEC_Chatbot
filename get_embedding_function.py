from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.embeddings.bedrock import BedrockEmbeddings
from langchain.embeddings import OpenAIEmbeddings


def get_embedding_function(embedding_type):
    """
    Call the embedding model for vectorized database. Currently utilizing Ollama Embeddings is set to 'nomic-embed-text' 
    model. Different models can be added. 
    Args:
    - embedding_type (str): The type of embedding model to use. Accepts 'OllamaEmbeddings' for the Ollama embeddings model.
    Returns:
    - embeddings: An instance of the specified embedding model.
    Raises:
    - Exception: If the specified embedding type is not recognized.
    """

    if embedding_type == 'OllamaEmbeddings':
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    else:
        raise Exception("Embedding Function Not Recognized")

    return embeddings