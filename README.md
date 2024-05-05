# Chat Bot
## _A kool chatbot that chats with your website_

chat-with-websites contains the source code for a chatbot that will chat with any website given its url. It is built on streamlit,langchain,openAI and vectorDB.

## Features

- Type any website and get ready to chat with it.
- The chat bot is history aware, so no need to worry about what you asked in an earlier conversation. The chatbot knows it all
- Uses powerful ChatOpenAI that produces accurate answers to your queries.

## Tech

This chatbot uses below tech stack

- [Streamlit] - Easy to use python framework to quickly spin up maching learning UIs!
- [langchain] - A powerful framework to interact with the AI models of your choice
- [chromaDB] - A lightweight vector database to store all the embedding goodness.
- [openAI] - ChatOpenAI model as llm to get the most accurate results from the contextual documents.

## Installation

### Create a virtual environment
- Make sure you have atleast python 3.10 installed on your system and git a client
- Execute command ```git clone https://github.com/pradeeptyagi23/chat-with-websites.git```
- This will create a folder chat-with-websites on the path where the git clone command was executed
- ```cd chat-with-websites```
- Create a virtual environment with the command ```python -m venv venv```
- This will create a virtual environment 'venv' inside the project folder
- Activate the virtual environment with command ```source venv/bin/activate```

### Install dependencies
- Now from the project root folder, run the command ```pip install -r requirements.txt```
- This will install all required dependencies.
- Create .env in the project root folder to add the openAI API key. (Checkout .env.example to see an example)

### Run the streamlit app
- Next, execute command ```streamlit run src/app.py``` from the project root folder.
- This will open up the chatbot window on your localhost
- Happy chatting with the chatbot.

![chatbot](https://github.com/pradeeptyagi23/chat-with-websites/assets/8380756/adf5ea20-346b-447f-9a02-55562e0d92d8)

