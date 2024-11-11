import google.generativeai as genai
import streamlit as st
from googletrans import Translator
import streamlit.components.v1 as components
import os
import speech_recognition as sr
import pyttsx3

st.title("AI-powered safetybot 🤖")
translator_obj=Translator()
recg=sr.Recognizer()
genai.configure(
    api_key='AIzaSyDazx17rjwxGfHmizIqlL9aOmswbCw2oYo'
)
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 850,
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  system_instruction='''
    you are a the actual friend of the user who will provide the mental support to the user when you feel 
    that the user is distressed, you will answer to prevent any kind of suicidial thoughts of the user and you can also recommend 
    some books or provide the url of some websites for mood refreshing songs.If you are asked about route recommendation you will 
    provide the exact answer and you will provide the exact google maps' url that will redirect the user to the specified route 
    requested by the user. If the user ask you about any other things you will also provide the indepth answer to the question.
    if you are asked to provide certain emergency numbers then response by searching on the internet.
'''
)

def translate(satement,target_lang):
    if target_lang!="en":
        return translator_obj.translate(satement,dest=target_lang).text
    return satement

def convert_role(role):
    if role=="model":
        return "ai"
    else:
        return "user"
    
def show(prompt):
     with st.chat_message("ai"):
        with st.spinner("generating....."):
            res=st.session_state.msg.send_message(prompt)
            trans_res=translate(res.text,st.session_state.user_lang)
            st.markdown(trans_res)


if "user_lang" not in st.session_state:
    st.session_state.user_lang="en"

if "message" not in st.session_state:
    st.session_state.message=model.start_chat(
        history=[
            {
                "role":"model",
                "parts":"Hi I am your AI assistant how can i help you?"
            }
        ]
    )

   
if "msg" not in st.session_state:
    st.session_state.msg=model.start_chat(
        history=[
            {
                "role":"model",
                "parts":"hey how can i help you? i will do my best to serve you..."
            }
        ]
    )

for message in st.session_state.msg.history:
    with st.chat_message(convert_role(message.role)):
        st.write(message.parts[0].text)

if prompt:=st.chat_input(''):
    translated_text=translator_obj.translate(prompt,dest='en').text if st.session_state.user_lang!="en" else prompt
    st.chat_message('user').markdown(prompt)
    show(translated_text)




   
