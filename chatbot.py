import google.generativeai as genai
import streamlit as st
import time
import random
from googletrans import Translator

context={
    "last":None,
    "await":False
}
st.title("AI-Powered safetybot")
translator=Translator()
genai.configure(api_key='AIzaSyChMO-Fy3iGMGm89meke4d-P5ebcG_sX0Q')
generation_config={
    "temperature": 2,
    "max_output_tokens": 800,
    "top_k": 50,
    "top_p": 0.95,
    "candidate_count": 1
}
#and you may also provide the Google Maps URL with for the specified route with different transport mediums#
model=genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=
    '''
    You are a helpful assistant who will provide in-depth answers to the user's queries related
    to any location or may ask you to recommend the route or ask you about details of any place. You will provide in-depth answers
    for all these. in case if you are asked to show or recommend route, you will provide the correct Google Maps URL along with your response 
    
    If asked to show nearby locations or safe places, respond with the Google Maps link to redirect users to
    their saved places: Ensure the response is clear that users need to be logged in to view their personal saved places.
    If asked to generate or recommend music, assure the user you will do something for them without naming specific songs currently.
    If you sense the user is very distressed, offer some mood-relaxing songs without naming them.
    '''
)
def translate(satement,target_lang):
    if target_lang!="en":
        return translator.translate(satement,dest=target_lang).text
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
            #time.sleep(0.5/80)


def show_route(prompt):
    with st.chat_message("ai"):
        with st.spinner("generating response...."):
            response=st.session_state.msg(prompt)
            #linked=make_url(response.text)
            st.markdown(response.text)

def typewriter(prompt):
    s=prompt.split()
    con=st.empty()
    for i in range(len(s)+1):
        c=" ".join(s[:i])
        con.markdown(c)
        time.sleep(0.5/20)

if "user_lang" not in st.session_state:
    st.session_state.user_lang="en"

    
if "msg" not in st.session_state:
    #st.chat_message('ai').markdown("hey how can i help you? i will do my best to serve you...")
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
    translated_text=translator.translate(prompt,dest='en').text if st.session_state.user_lang!="en" else prompt
    st.chat_message('user').markdown(prompt)
    show(translated_text)

# Example of displaying the Google Maps link as a clickable hyperlink in Streamlit
#st.write("Click [here](https://www.google.com/maps/dir/Kolkata,+West+Bengal/Delhi,+India) to view the route in Google Maps.")

   
