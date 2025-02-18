import os
import streamlit as st
from app_tab1 import render_story_tab
from vertexai.preview.generative_models import GenerativeModel
import vertexai
import logging
from google.cloud import logging as cloud_logging

logging.basicConfig(level=logging.INFO)
log_client = cloud_logging.Client()
log_client.setup_logging()

PROJECT_ID = os.environ.get('PROJECT_ID')
LOCATION = os.environ.get('REGION')
vertexai.init(project=PROJECT_ID, location=LOCATION)

@st.cache_resource
def load_model():
    return GenerativeModel("gemini-pro")

st.header("Vertex AI Gemini API Damo PoC", divider="rainbow")
text_model_pro = load_model()

render_story_tab(text_model_pro)
