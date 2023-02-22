import streamlit as st
import azure_read
from PIL import Image
from io import BytesIO
from azure_read import recognize_text

ENDPOINT = "https://reciept-recogn.cognitiveservices.azure.com/"
SUB_KEY = "7aca8e57fee94c4ea586c4fb16e421be"

# Display a file uploader widget
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# When the user clicks the "Recognize Text" button...
if st.button("Recognize Text") and uploaded_file is not None:
    # Call the recognize_text function to get the recognized text
    text = recognize_text(SUB_KEY, ENDPOINT, uploaded_file)
    # Display the recognized text
    st.write(text)