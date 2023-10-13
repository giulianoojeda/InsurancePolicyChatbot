<h1 align="center">
📖 Policy Pro Insurance LLM Agent
</h1>

![UI](demo_app/assets/logo.png?raw=true "Policy Pro Insurance LLM Agent")

## 🔧 Features

- Streamlit App integrated with `openai` API for the Policy Pro chatbot.
- A ChatBot specifically designed for insurance policies using Streamlit.
- Docker Support for reproducibility and ease of deployment.
- Deployment options for Streamlit Public Cloud.

This repo contains the main application logic for the Policy Pro LLM Insurance chatbot.

## How is the code organized?

The code is organized into two main sections:

- `demo_app`: Contains the main application logic for the Policy Pro LLM Insurance chatbot.
- `demo_app/assets`: Contains the assets used for the application.
- `demo_app/chroma`: Contains the chroma vector parquet files.
- `demo_app/src`: Contains the source code for the application.
- `demo_app/src/agent`: Contains the agent logic for the application.
- `demo_app/src/agent/tools`: Contains the tools used by the agent.
- `notebooks`: Contains the notebooks used for development and testing.

## Configuration

The application can be configured using the `.env` file. The following variables are available:

AWS_ACCESS_KEY_ID - AWS Access Key ID (Example: my-access-key-id)
AWS_SECRET_ACCESS_KEY - AWS Secret Access Key (Example: my-secret-access-key)
OPENAI_API_KEY - OpenAI API Key (Example: my-openai-api-key)
TEMPERATURE - Sets temperature in OpenAI (Default: 0)
SMART_LLM_MODEL - Smart language model (Default: gpt-4)
FAST_LLM_MODEL - Fast language model (Default: gpt-3.5-turbo)
GOOGLE_API_KEY - Google API key (Example: my-google-api-key)
CUSTOM_SEARCH_ENGINE_ID - Custom search engine ID (Example: my-custom-search-engine-id)

## 💻 Running Locally

1. **Clone the Repository**📂
```bash
git clone https://github.com/giulianoojeda/InsurancePolicyChatbot.git
```

2. **Install Dependencies and Activate Virtual Environment**🔨
```bash
poetry install
poetry shell
```

3. **Run the Streamlit Server**🚀
```bash
streamlit run app/main.py 
```

### Run App using Docker
This project is Dockerized for easier setup and deployment. To utilize Docker:

- Build the Docker image:
```bash
docker  build . -t policypro-insurance-agent:latest
```

- Run the Docker container:
```bash
docker run -d --name policypro-insurance-agent -p 8501:8501 policypro-insurance-agent
```

or using docker-compose:
```bash
docker-compose up
```

### Deploy App on Streamlit Public Cloud
Deploy the app on Streamlit Public Cloud using your GitHub repository. Tutorial [here](https://docs.streamlit.io/en/stable/deploy_streamlit_app.html#deploy-your-app-to-streamlit-sharing).


## DISCLAIMER
When integrating with the `openai` API, you may incur charges based on usage. Ensure you're aware of any associated costs when deploying or testing extensively.
