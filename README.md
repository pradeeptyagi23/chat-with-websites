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

Currently it doesnt support any fancy way of installation as this is a work in progress.
But below packages are installed  before running the code.
- pip install beautifulsoup4 (scraping the website)
- pip install python-dotenv
- pip install streamlit(user interface)
- pip install langchain(interface with the model)
- pip install langchain_openai(langchain partner package for openai)
- pip install chromadb

Also , dont forget to add your openAI API key in the .env of your project root as :
OPENAI_API_KEY=<openAI-API-Key>

Once all the required packages are installed and the open AI API key is specified.
It can run as 
```
streamlit run src/app.py
```
This will open the chabot on the localhost.And is ready to use

![image](https://github.com/pradeeptyagi23/chat-with-websites/assets/8380756/dda1444c-4a39-4e0c-8230-4e5c3e835a79)
