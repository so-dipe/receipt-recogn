


import streamlit as st
from PIL import Image
from azure_read import recognize_text, plot_bounding_boxs

from dotenv import load_dotenv
import os

# from streamlit_cropper import st_cropper

load_dotenv()  # Load environment variables from .env file


ENDPOINT = os.environ.get('ENDPOINT')
SUB_KEY = os.environ.get('SUBSCRIPTION_KEY')

# Display a file uploader widget
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# When the user clicks the "Recognize Text" button...
if uploaded_file is not None:
    #Display Image
    image = Image.open(uploaded_file)
    width = st.slider("Move to Zoom Image", 100, 1000)
    st.image(image, caption='Uploaded Image', width=width)
    # with st.expander("See Zoomed Image"):
    # st.image(image, caption='Uploaded Image', width=1000)

    if st.button("Recognize Text"):
        # Call the recognize_text function to get the recognized text
        texts, lines, bb = recognize_text(SUB_KEY, ENDPOINT, uploaded_file)
        # Display the recognized text
        st.write(texts)
        image = plot_bounding_boxs(bb, image)
        st.image(image, caption='Bounding Box Image')
    