import argparse
import os
import shutil
from JSON_Manage import add_data_info_to_database, remove_database
from langchain.document_loaders.pdf import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from get_embedding_function import get_embedding_function
from langchain.vectorstores.chroma import Chroma

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database. Databse Reset Is Determined By --chroma_db_name flag")
    parser.add_argument("--embedding_function", default="OllamaEmbeddings", type=str, help="Select The Embedding Function")
    parser.add_argument("--chroma_db_name", default="chroma", type=str, help="Select The Database Identifier To Create A New One Or Add To An Old One")
    parser.add_argument("--data_path", default="data", type=str, help="Select the directory where data is stored in")
    args = parser.parse_args()

    #Database in chroma name to use
    chromadatabase = args.chroma_db_name
    data_dir = args.data_path

    #Reset chroma database based off of the chromatabase name 
    if args.reset:
        print(f"Removing database: {chromadatabase}")
        clear_database(chromadatabase)
    
    else:
        embedding = args.embedding_function
        #Load documents into dataset
        documents = load_documents(data_dir)
        #Chunk the documents
        chunks = chunk_documents(documents)
        #Add chunks into chroma database
        add_to_chroma(chunks, embedding, chromadatabase, data_dir)
    
def load_documents(data_dir):
    """
    Loads documents from a specified directory.
    Args:
        data_dir (str): The directory containing the documents to be loaded.
    Returns:
        list[Document]: A list of loaded documents.
    """

    document_loader = PyPDFDirectoryLoader(data_dir)
    return document_loader.load()


def chunk_documents(documents: list[Document]):
    """
    Chunks documents from a list of loaded documents
    Args:
        documents (list[Document]): A list of documents to be chunked.
    Returns:
        list[Document]: A list of document chunks.
    """
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )

    chunks = text_splitter.split_documents(documents)

    return chunks

def add_to_chroma(chunks: list[Document], embedding, chromadatabase, data_dir):
    """
    Adds document chunks to a Chroma database.
    Args:
        chunks (list[Document]): A list of document chunks to be added.
        embedding (str): The embedding function to be used.
        chromadatabase (str): The Chroma database name and directory.
        data_dir (str): The directory containing the documents.

    Returns:
        None
    """

    db = Chroma(
        persist_directory=chromadatabase, embedding_function=get_embedding_function(embedding)
    )

    #Calculate Page IDs.
    chunks_with_ids = calculate_chunk_ids(chunks)

    existing_items = db.get(include=[])
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    #Only add documents that don't exist in the DB.
    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    #Adding only new chunks
    if len(new_chunks):
        print(f"Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
        db.persist()
    else:
        print("No new documents to add")

    all_data_paths = [os.path.join(data_dir, file) for file in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, file))]
    
    add_data_info_to_database(chromadatabase, all_data_paths, len(chunks_with_ids), embedding)

def calculate_chunk_ids(chunks):
    """
    Calculates unique IDs for document chunks based off of path of file and which chunk of the file it is from.
    
    Args:
        chunks (list[Document]): A list of document chunks.
    Returns:
        list[Document]: A list of document chunks with unique IDs.
    """


    last_document_id = None
    current_chunk_num = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        #page = chunk.metadata.get("page")
        document_id = f"{source}"

        # If the page ID is the same as the last one, increment the index.
        if document_id == last_document_id:
            current_chunk_num += 1
        else:
            current_chunk_num = 0

        # Calculate the chunk ID.
        chunk_id = f"{document_id}:{current_chunk_num}"
        last_document_id = document_id

        # Add it to the page meta-data.
        chunk.metadata["id"] = chunk_id

    return chunks


def clear_database(databasePath):
    """
    Clears the specified database directory.
    Args:
        databasePath (str): The path to the database directory to be cleared.
    Returns:
        None
    """
    if os.path.exists(databasePath):
        shutil.rmtree(databasePath)
        remove_database(databasePath)


if __name__ == "__main__":
    main()