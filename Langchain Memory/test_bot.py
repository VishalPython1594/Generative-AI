import streamlit as st
import pandas as pd
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the API key
key = os.getenv("GOOGLE_API_KEY")
print(key)

chat_model = ChatGoogleGenerativeAI(api_key=key, model='gemini-1.5-flash')

# Retrieves the history for a particular session using session id
def get_messages_history_from_db(session_id):
    chat_history = SQLChatMessageHistory(session_id=session_id, connection='sqlite:///C:/Users/DeLL/Documents/Data Science/Gen AI/sql_chat_data/new_database.db')
    # Get the raw messages as a list
    return chat_history  # This should return a list of messages, not an object with .messages attribute

# Creating a chat template
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
chat_template = ChatPromptTemplate.from_messages([('system', '''You name is Freddy and You are known to be a very helpful, interactive 
                              and polite instructor concerned with answering queries and solving doubts
                              related to Data Science and AI. If there doubt or question is not relevant to
                              data science and AI, tell them politely to ask the questions
                              relevant to only Data Science and AI. Your responses should be simple and there
                              should be examples with your answers (if applicable). Please answer in
                              detail and in an explainatory way. If you are
                              not sure about a certain topic or question, don't assume anything
                              and tell the user that you are sorry and are not sure of that 
                              particular topic by giving them suitable links to refer (if applicable).
                              Your responses should not contain any sexist, racist, inappropriate or
                              biased remarks.'''),
                                                  MessagesPlaceholder(variable_name='history'),
                                                  ('human', '{human_input}')])

# creating a chain
chain = chat_template | chat_model

# bringing the memory and the chain (pipeline) together
from langchain_core.runnables import RunnableWithMessageHistory
conversational_chain = RunnableWithMessageHistory(chain,
                                                  get_messages_history_from_db,
                                                  history_messages_key='history',
                                                  input_messages_key='human_input')

# configuring the session id and invoking the chain
st.title('Freddy the AI Bot')

user_id = st.text_input("Please tell me your name to start the conversation:")

if user_id:
    config = {'configurable': {'session_id': user_id}}

    # Retrieve conversation history from the database and display it
    chat_history = get_messages_history_from_db(user_id)

    # Display entire conversation (messages) in the chat
    for message in chat_history.messages:
        # Assuming each message in the list is a dictionary or object that contains 'role' and 'content'
        if isinstance(message, dict) and 'role' in message and 'content' in message:
            if message['role'] == "human":
                st.chat_message("user").write(message['content'])
            else:
                st.chat_message("assistant").write(message['content'])

    st.chat_message('assistant').write(f"Hi {user_id}! How may I help you?")

    user_input = st.chat_input()

    if user_input:
        input_prompt = {'human_input': user_input}

        st.chat_message('user').write(user_input)
        
        response = conversational_chain.invoke(input_prompt, config=config)
    
        st.chat_message('assistant').write(response.content)

        # Optionally save the context after the response
        # memory.save_context(inputs={'human_input': user_input}, outputs={'output': response.content})
