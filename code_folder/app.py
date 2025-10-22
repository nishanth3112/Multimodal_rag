import streamlit as st
import pandas as pd
import numpy as np
from langchain_community.vectorstores.faiss import FAISS
from streamlit_chat import message
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
import os
import json
from utils import *
from langchain_community.chat_models import BedrockChat
from langchain_community.embeddings import BedrockEmbeddings

import boto3

# Initialize a boto3 client for AWS Bedrock
bedrock = boto3.client('bedrock-runtime')

# Define embeddings using the Bedrock client and a specific model
embeddings = BedrockEmbeddings(
    client=bedrock,
    model_id="amazon.titan-embed-text-v2:0"
)

# Set model parameters
model_kwargs = {
    "max_tokens": 2048,
    "temperature": 0.0,
    "stop_sequences": ["\n\nHuman"],
}

# Initialize the language model (LLM) with the specified Bedrock chat model
llm = BedrockChat(
    client=bedrock,
    model_id="anthropic.claude-3-sonnet-20240229-v1:0",
    model_kwargs=model_kwargs,
)

# Load the FAISS vector store from local storage
db = FAISS.load_local("output/faiss_index", embeddings, allow_dangerous_deserialization=True)

# Initialize session state for chat
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'images' not in st.session_state:
    st.session_state['images'] = []
if 'assistant_response' not in st.session_state:
    st.session_state['assistant_response'] = []

# Streamlit app title
st.title("Food Recommendation Assistant")

# User input for text
user_input = st.text_input("You: ", " ", key="input")
original_input = user_input[:]

# Image upload input
uploaded_image = st.file_uploader("Upload an image to enhance search", type=["png", "jpg", "jpeg"])

# Button to send the input
send_button = st.button("Send")
image = "no"

# Process input when the send button is clicked
if send_button and (user_input or uploaded_image):
    if uploaded_image:
        image = 'yes'
        encoded_image = base64.b64encode(uploaded_image.read()).decode('utf-8')
        st.session_state.images.append(encoded_image)
        
        # Describe the uploaded image using the language model
        image_description = describe_input_image(encoded_image, llm)
        
        # Enhance user input with image description
        user_input = 'I am looking for this dish, recommend similar dishes: ' + user_input + " " + image_description

    # Add user input to chat history
    st.session_state.past.append(user_input)

    # Create an enhanced search query using the user input
    enhanced_search_query = enhance_search(user_input, llm)
    enhanced_search_query = clean_text(enhanced_search_query)

    # Perform similarity search using FAISS
    results = db.similarity_search(user_input, k=5)
    print("Results generated!")

    # Compile context from search results
    context = ""
    for doc in results:
        context += doc.page_content + "\n\n"

    # Generate a chatbot response using the assistant function
    chatbot_response = assistant(context, user_input, llm)
    print(chatbot_response)

    # Parse the chatbot response
    chatbot_response = json.loads(chatbot_response)

    # Extract recommendation and response from the chatbot output
    recommendation = chatbot_response.get('recommendation')
    response = chatbot_response.get('response')

    # Append the response to chat history
    st.session_state.assistant_response.append(response)

    if recommendation == 'yes':
        # If a recommendation is needed
        if image == 'yes':
            original_input = user_input[:]

        # Generate recommendations based on user preferences
        rec_response, relevant_images = recommend_dishes_by_preference(results, original_input, llm)
        
        # Append the recommendation response to chat history
        st.session_state.generated.append((rec_response, relevant_images))
        print("Rec response generated")
    else:
        # Append normal response to chat history
        st.session_state.generated.append((response, []))

    # Display chat history in a reversed order (latest messages first)
    for i in range(len(st.session_state['generated']) - 1, -1, -1):
        # Display user message
        message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')

        # Display bot response and image
        response, images = st.session_state["generated"][i]

        if isinstance(response, list):  # If it's a list, it's a recommendation
            for j, rec in enumerate(response):
                # Use columns to align text and image side by side
                col1, col2 = st.columns([3, 1])
                image_path = list(images.keys())[j]
                metadata = images[image_path]

                with col1:
                    with st.chat_message("assistant"):
                        st.markdown(f"**{rec}**")
                        st.markdown(f"**Name:** {metadata['menu_item_name']}")
                        st.markdown(f"**Restaurant:** {metadata['restaurant_name']}")
                        st.markdown(f"**Nutrition:** {metadata['nutrition']}")
                        st.markdown(f"**Calories:** {metadata['calories']}")
                        st.markdown(f"**Price: USD** {metadata['price']}")
                        st.markdown(f"**Serves:** {metadata['serves']}")
                        st.markdown(f"**Rating:** {metadata['average_rating']}")
                with col2:
                    st.image('data/'+ image_path, use_column_width=True)
        else:
            # Just display the normal response
            with st.chat_message("assistant"):
                st.markdown(f"**{response}**")
