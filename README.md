#   Introduction
SEC and FINRA documents establishing rules and regulation for public and private securities exchanges are dense and difficult to interpret without proper legal training and contexts. This chatbot uses LLM + RAG framework with the context of the SEC documents from 1933, 1934 and Dodd-Frank Wall Street Reform & Consumer Protection Act to answer complex financial questions.
This project also contains the methods to add any pdf files to a new user defined vector database seperate from the SEC documentation, or to further add to the current SEC documentation in the database. Furthermore, it provides visualization for what documents are in the database through a JSON file. Finally, there is a very simple frontend for the dfault SEC chatbot with the context of the default SEC vector database. If custom databases are created using this framework, the user can utilize the chatbot through the command line.

#  Chatbot Usage - Adding to Vectorized Database
Calling the Add_To_Database.py script adds pdf documents to the vectorized database to be queried later. The script supports the following arguments:<br />
-data_path: path to the data_directory of pddf files to add to vector database<br />
-chroma_db_name: assigns identification to the vectorized database<br />
-embedding_function: method utilized for the embedding function for chunking and querying, currently only supports Ollama nomic-text-embedding<br />
-reset: given the chroma_db_name argument along with it, will remove that database<br />

A databases.json file exists that updates along with adding or removing files from databases and databases<br />

#  Chatbot Usage - Prompting chatbot
The user can use the querey_vector_database.py script to chat with the chatbot. The script supports the following arguments:<br />
-prompt: takes in the prompt to ask the LLM<br />
-embedding_function: embedding function to use for prompt and querying against vector database, whatever embedding was used for the database needs to be consistent<br />
-chroma_db_name: the database id to be finding the context from<br />

# Chatbot Usage - Default chatbot UI
If the user is using the default SEC database already created, they can use the basic frontend built with Flask to ask their question and receive an answer. To launch the front end, run App.py and copy the local host address displayed within the terminal in a web browser. From there the user can ask any question to the SEC chatbot.

#  Current Databases
Two databases are already setup, one having the SEC documentation named "chromaSEC" and the other having banana bread and carrot cake recipes named "chromaRecipe". Both use the "nomic-embed-text" embedding.




