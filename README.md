
# Chat with Website using Gen AI

An AI-powered tool that allows users to interactively query website content by scraping, processing, and analyzing webpage data. Users can input a website URL, and the tool provides answers based on the extracted information.

## Features
- **Data Collection**: Scrapes content from specified website URLs.
- **Data Processing**: Cleans and structures text, removing HTML/CSS tags.
- **Conversational AI**: Uses a language model to answer questions about the website content.
- **User-Friendly Interface**: Built with Streamlit for easy interaction.

## Getting Started

### Prerequisites
- Python 3.x
- Required libraries:
  - `streamlit`
  - `requests`
  - `beautifulsoup4`
  - `transformers` (Hugging Face)
  
### Installation
1. Create `.env` file and add `Hugging-Face-API`

2. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/chat-with-website-gen-ai.git
   cd chat-with-website


3. Create Enviroment
    ```bash
    python -m venv myenv
4. Activate Enviroment
    ```bash
    myenv/Scripts/Activate
5. Run Streamlit App
    ```bash
    streamlit run src/app.py

### Use
#### 1. Enter a website URL, and the app will scrape and process its content.

#### 2. Interact with the website's content by asking questions in the chat box.

### Project Structure
1. `app.py:` Main application script to run the Streamlit interface.
2. `scraper.py:` Contains the scraping logic to extract website content.
3. `gen_ai.py:` Handles interaction with the language model for generating responses.