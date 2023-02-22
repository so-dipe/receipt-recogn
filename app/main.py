import streamlit as st
from PIL import Image
from azure_read import recognize_text, plot_bounding_boxs
import copy
from dotenv import load_dotenv
import os

# from streamlit_cropper import st_cropper

load_dotenv()  # Load environment variables from .env file


ENDPOINT = os.environ.get('ENDPOINT')
SUB_KEY = os.environ.get('SUBSCRIPTION_KEY')

# Display a file uploader widget
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# When the user clicks the "Recognize Text" button...
# if uploaded_file is not None and st.button("Recognize Text"):
#     st.write(type(uploaded_file))
#     # with st.expander("See Zoomed Image"):
#     # st.image(image, caption='Uploaded Image', width=1000)
#     # Call the recognize_text function to get the recognized text
#     texts, lines, bb = recognize_text(SUB_KEY, ENDPOINT, uploaded_file)
#     # Display the recognized text
#     st.write(texts)
#     #Display Image
#     image = Image.open(uploaded_file)
#     width = st.slider("Move to Zoom Image", 100, 1000)
#     st.image(image, caption='Uploaded Image', width=width)
#     image = plot_bounding_boxs(bb, image)
#     st.image(image, caption='Bounding Box Image')

if uploaded_file is not None:
    file_upload = copy.copy(uploaded_file)
    image = Image.open(file_upload)
    width = st.slider("Move to Zoom Image", 100, 1000)
    st.image(image, caption='Uploaded Image', width=width)

    # st.session_state['results'] = {"lines":"", "text":"", "bb":""}
    if st.button('Extract Text'):
        texts, lines, bb = recognize_text(SUB_KEY, ENDPOINT, uploaded_file)
        # results['text'] = texts
        # results['lines'] = lines
        # results['bb'] = bb
        st.session_state['results'] = {"lines":lines, "text":texts, "bb":bb}
    col1, col2 = st.columns(2)
    with col1:
        st.write(st.session_state['results'])
    with col2:
        image = Image.open(file_upload)
        image = plot_bounding_boxs(st.session_state['results']['bb'], image)
        width = st.slider("Move to Zoom Image", 100, 500)
        st.image(image, caption='Bounding Box Image', width=width)
    