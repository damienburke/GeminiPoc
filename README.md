# Gemini Overview

Gemini is a family of generative AI models that is designed for multimodal use cases. It comes in three sizes: Ultra,
Pro and Nano. Gemini 1.0 Pro is available for developers and enterprises to build for your own use cases. Gemini 1.0 Pro
accepts text as input and generates text as output. There is also a dedicated Gemini 1.0 Pro Vision multimodal endpoint
that accepts text and imagery as input, and generates text as output. SDKs are available to help you build apps in
Python, Android (Kotlin), Node.js, Swift and JavaScript.

On Google Cloud, the Vertex AI Gemini API provides a unified interface for interacting with Gemini models. The API
supports multimodal prompts as input and output text or code. There are currently two models available in the Gemini
API:

Gemini 1.0 Pro model (gemini-pro): Designed to handle natural language tasks, multiturn text and code chat, and code
generation.

Gemini 1.0 Pro Vision model (gemini-pro-vision): Supports multimodal prompts. You can include text, images, and video in
your prompt requests and get text or code responses.

Vertex AI is a machine learning (ML) platform that lets you train and deploy ML models and AI applications, and
customize large language models (LLMs) for use in your AI-powered applications. Vertex AI allows for customization of
Gemini with full data control and benefits from additional Google Cloud features for enterprise security, safety,
privacy and data governance and compliance.

# PoC Overview

* Python app, using the Streamlit framework
* Interacts with the Gemini 1.0 Pro model (gemini-pro) using the Vertex AI Gemini API
* The app is containerized and deployed on Cloud Run

### PoC in depth

* The app first initializes the Vertex AI SDK passing in the values of the PROJECT_ID, and REGION environment variables.
* It then loads the gemini-pro model using the GenerativeModel class that represents a Gemini
  model. This class includes methods to help generate content from text, images, and video.
* The app renders the UI.
* The generate_prompt function generates the text prompt that is supplied to the Gemini API. The prompt string is
  created by concatenating user entered values in the tab UI for the character of the story, and options such as the
  story length (short, long), creativity level (low, high), and the story premise.
* The function also returns a temperature value based on the selected creativity level of the story. This value is
  supplied as the temperature configuration parameter to the model, which controls the randomness of the model's
  predictions. The max_output_tokens configuration parameter specifies the maximum number of output tokens to generate
  per message.
* To generate the model response, a button is created in the tab UI. When the button is clicked, the
  get_gemini_pro_text_response function is invoked, which we will code in the next step in the lab.
* The get_gemini_pro_text_response function uses the GenerativeModel and some of the other classes from the
  vertexai.preview.generative_models package in the Vertex AI SDK for Python. From the generate_content method of the
  class, a response is generated using the text prompt that is passed to the method.
* A safety_settings object is also passed to this method to control the model response by blocking unsafe content. The
  sample code in this lab uses safety setting values that instructs the model to always return content regardless of the
  probability of the content being unsafe. You can assess the content generated, and then adjust these settings if your
  application requires more restrictive configuration. To learn more, view the safety settings documentation.

# GCP Setup

```bash
PROJECT_ID=$(gcloud config get-value project)
REGION=us-east4
SERVICE_NAME='gemini-poc'
AR_REPO='poc-repo'

echo "PROJECT_ID=${PROJECT_ID}"
echo "REGION=${REGION}"
echo "SERVICE_NAME=${SERVICE_NAME}"
echo "AR_REPO=${AR_REPO}"
```

### Cloud Run Deployment

```bash
gcloud builds submit --tag "$REGION-docker.pkg.dev/$PROJECT_ID/$AR_REPO/$SERVICE_NAME"
```

```bash
gcloud run deploy "$SERVICE_NAME" \
  --port=8080 \
  --image="$REGION-docker.pkg.dev/$PROJECT_ID/$AR_REPO/$SERVICE_NAME" \
  --allow-unauthenticated \
  --region=$REGION \
  --platform=managed  \
  --project=$PROJECT_ID \
  --set-env-vars=PROJECT_ID=$PROJECT_ID,REGION=$REGION
```

# Dev Notes

### Set up a Python virtual environment

Create a virtual environment on top of the existing Python installation, so that any packages installed in this
environment are isolated from the packages in the base environment. When used from within a virtual environment,
installation tools such as pip will install Python packages into the virtual environment.

```bash
mkdir ~/gemini-poc && cd ~/gemini-poc
python3 -m venv gemini-streamlit
source gemini-streamlit/bin/activate
```

### Install application dependencies

A Python requirements file is a simple text file that lists the dependencies required by your project. To start, there
are three modules we need in our requirements file.

Our app is written using Streamlit, an open-source Python library that is used to create web apps for machine learning
and data science. The app uses the Vertex AI SDK for Python library to interact with the Gemini API and models.

### Testing the app

```bash
streamlit run app.py \
--browser.serverAddress=localhost \
--server.enableCORS=false \
--server.enableXsrfProtection=false \
--server.port 8080
```

To launch the app home page in your browser, click web preview in the Cloud Shell menubar, and then click Preview on
port 8080.
