import streamlit as st
import pandas as pd
import google.generativeai as genai
with open(r"C:\Users\DeLL\Documents\Data Science\Gen AI\Building  conversational chat bot and intro to Gemini\Google API Key.txt") as f:
    key = f.read().strip()
genai.configure(api_key = key)
model = genai.GenerativeModel(model_name = 'gemini-1.5-flash', system_instruction = '''
                              You name is Freddy and You are known to be a very helpful, interactive 
                              and polite instructor concerned with answering queries and solving doubts
                              related to Data Science and AI. If there doubt is not relevant to
                              data science and AI, tell them polietly to ask the questions
                              relevant to the topic. Your responses should be simple and there
                              should be examples with your answers (if applicable). If you are
                              not sure about a certain topic or question, dont assume anything
                              but tell the user that you are sorry and are not sure of that 
                              particular topic by giving them suitable links to refer (if applicable).
                              Your responses should not contain any sexist, racist, unappropriate or
                              biased remarks.
                              ''')
st.title('Freddy the AI Bot')
st.chat_message('assistant').write('Hi! How may i help you?')
history = []
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
    
for msg in st.session_state['messages']:
    st.chat_message(msg['role']).write(msg['content'])

user_input = st.chat_input()
if user_input:
    st.chat_message('user').write(user_input)
    history.append(f"User: {user_input}")
    conversation_history = "\n".join(history)
    response = model.generate_content(conversation_history)
    history.append(response.text)
    st.chat_message('assistant').write(response.text)
    

