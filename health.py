### Health Management App
from dotenv import load_dotenv
load_dotenv()   ## Loading all the environment variables
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to Load Gemini Pro Vision API and get responses
model=genai.GenerativeModel("gemini-pro-vision")

def get_gemini_response(input,image, prompt):
    response=model.generate_content([input,image[0],prompt])
    return response.text

def input_image_details(upload_file):
    if upload_file is not None:
        # Read the file into bytes
        bytes_data=upload_file.getvalue()

        image_parts=[
            {
                "mime_type":upload_file.type, # Get the mimetype of the uploaded file
                "data":bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No File Uploaded")

## initializing our Streamlit app

st.set_page_config(page_title="Gemini Health App")

st.header("Gemini Health App")
input=st.text_input("Input prompt: ",key="input")
upload_file = st.file_uploader("Choose an image of the Invoice... ", type=["jpg","jpeg",'png'])

if upload_file is not None:
    image=Image.open(upload_file)
    st.image(image,caption="uploaded Image.", use_column_width=True)

submit=st.button("Tell me the Total Calories")

input_prompt='''
    You are an expert in Nutritionist where you need to see the food items from the image and
    calculate the total calories, also provide the details of every food items with calories intake
    in below format
    1. Item 1 - no of calories
    2. Item 2 - no of calories
    ----
    ----
    '''

# If Submit button is clicked

if submit:
    image_data=input_image_details(upload_file)
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader('The Response is')
    st.write(response)