import streamlit as st
from api import *

st.set_page_config(
    page_title="Mr. Dave",
    layout="wide"
)
st.markdown("<h1 style='text-align: center;'>Mr. Dave 😬</h1>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align: center;'>Your next Comments Robot doesn't have to be on Weibo</h6>", unsafe_allow_html=True)

# Use session_state to store the state of the text_area and initialize as an empty string if it doesn't exist
if 'text_area_content' not in st.session_state:
    st.session_state.text_area_content = ""

prompt = st.text_area(' ', st.session_state.text_area_content, help = "Are you happy today?", height = 100)
st.session_state.text_area_content = prompt
send_text = st.button("send to Dave.", key = "send_prompt", help = "say hi to Dave?")

st.sidebar.subheader('Parameters')
max_length = st.sidebar.slider("Max Length", min_value = 1024, max_value = 8192, value = 2048, step = 1024, help = "Prompt Max Length")
temperature = st.sidebar.slider("Temperature", min_value = 0.10, max_value = 1.00, value = 0.95, step = 0.05)
top_p = st.sidebar.slider("Top_p", min_value = 0.1, max_value = 1.0, value = 0.7, step = 0.1)

st.sidebar.subheader(' ')
st.sidebar.subheader('stop the communication')
clear_button = st.sidebar.button("say bye to Dave", key = "stop", help = "bye,Dave")


# init session state
if 'persistent_output' not in st.session_state:
    st.session_state.persistent_output = []
    st.session_state.client, st.session_state.messages = init_staus()

# init counter
if 'counter' not in st.session_state:
    st.session_state.counter = 0

# add new of session_state
def add_to_persistent_output(text):
    st.session_state.persistent_output.append(text)

# Each time a button is clicked, the counter is incremented
def increment_counter():
    st.session_state.counter += 1

# semaphore staus
staus = st.session_state.counter

if send_text:
    if not prompt == "":
        # st.write()
        prompt_text = prompt
            
        response, st.session_state.messages = get_answer(st.session_state.client, st.session_state.messages, prompt_text, max_length, temperature, top_p, staus)
        increment_counter()
        print()    
        print(staus) # check print: num of this session rounds
            
        add_to_persistent_output("### User: ")
        add_to_persistent_output(prompt_text)
        add_to_persistent_output("### Comments Dave: ")
        add_to_persistent_output(response)

        print()   
        print(st.session_state.messages) # check print: messages of this session
            

if clear_button:
    st.session_state.persistent_output = []
    st.session_state.client, st.session_state.messages = init_staus()
    st.session_state.counter = 0
    st.markdown("<h4 style='text-align: center;'>Looking forward to seeing you again</h4>", unsafe_allow_html=True)

for output in st.session_state.persistent_output:
    st.write(output)