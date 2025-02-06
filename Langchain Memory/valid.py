import streamlit as st
import pandas as pd
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage
from langchain_community.chat_message_histories import SQLChatMessageHistory

from langchain_google_genai import ChatGoogleGenerativeAI
with open(r"C:\Users\DeLL\Documents\Data Science\Gen AI\Building  conversational chat bot and intro to Gemini\Google API Key.txt") as f:
    key = f.read().strip()
chat_model = ChatGoogleGenerativeAI(api_key = key, model = 'gemini-1.5-flash')

# Creating a chat template
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
chat_template = ChatPromptTemplate.from_messages([('system', '''You name is Freddy and You are known to be a very helpful, interactive 
                              and polite instructor concerned with answering queries and solving doubts
                              related to Data Science and AI. If there doubt or question is not relevant to
                              data science and AI, tell them polietly to ask the questions
                              relevant to only Data Science and AI. Your responses should be simple and there
                              should be examples with your answers (if applicable). If you are
                              not sure about a certain topic or question, dont assume anything
                              and tell the user that you are sorry and are not sure of that 
                              particular topic by giving them suitable links to refer (if applicable).
                              Your responses should not contain any sexist, racist, unappropriate or
                              biased remarks.'''),
                                                  MessagesPlaceholder(variable_name = 'chat_history'),
                                                  ('human', '{human_input}')])

#initializing memory
from langchain.memory import ConversationBufferMemory
memory = ConversationBufferMemory(memory_key = 'chat_history', return_messages = True)

#creating an output_parser
from langchain_core.output_parsers import StrOutputParser
output_parser = StrOutputParser()
##############

# creating a chain
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
# function to load message from memory

def get_message_from_memory(human_input):
    return memory.load_memory_variables(human_input)['chat_history']

chain = RunnablePassthrough.assign(chat_history = RunnableLambda(get_message_from_memory)) | chat_template | chat_model | output_parser

st.title('Freddy the AI Bot')

st.chat_message('assistant').write("Hi! How may I help you?")

user_input = st.chat_input()

if user_input:

    input_prompt = {'human_input' : user_input}

    st.chat_message('user').write(user_input)

    response = chain.invoke(input_prompt)

    st.chat_message('assistant').write(response)

# Check if the user input is valid (not None or empty)
   

    # Ensure response is valid (not None or empty)
   
        # Save the context in memory
    memory.save_context(
        input_prompt,  # Input as a string
        {'output':response}  # Response as a string
    )
        






















# Invoke the chain with human input and chat history
query = {'human_input' : 'explain the key difference between BERT and GPT models'}
response = chain.invoke(query)
print(response)
print()

##################

# Saving to memory
memory.save_context(query, {'output' : response})
