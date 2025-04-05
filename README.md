## **README (English Version)**

```markdown
# Private Q&A Bot Optimized

## Project Overview

**Private Q&A Bot Optimized** is a **Retrieval-Augmented Generation (RAG)**-based chatbot designed to manage a private knowledge base. The bot supports document upload, automatic vectorization, historical Q&A retrieval, and a seamless chat interface using Gradio. The system is optimized for local knowledge processing and allows for easy document-based querying and updates.

## Features

- **Streamlined Q&A Chat**: The bot supports dynamic, live, and context-aware conversations.
- **Document Management**: Allows users to upload documents (PDF, DOCX), which are automatically vectorized and added to the knowledge base.
- **Historical Retrieval**: View past questions and answers from the system’s database.
- **Modular Design**: The system is built with modular components, making it easy to extend or replace parts (such as the language model or document storage system).
- **Database Integration**: Uses SQLite for storing historical Q&A and file metadata, ensuring persistence.

## Project Structure

```
private_qa_bot_optimized/
├── app.py                        # Main launcher: Initializes the Gradio interface
├── config.py                     # Configuration file: paths, embedding model, etc.
├── requirements.txt              # List of required dependencies
├── chat_history.db               # SQLite database storing chat history (auto-generated)
├── ui/                           # User interface components
│   ├── layout.py                 # Page layout: Defines the tabs and component structure
│   ├── qa_page.py                # Q&A page: Takes user input and returns answers
│   ├── history_page.py           # History page: Displays past Q&A history
│   ├── library_page.py           # Document management page: Uploads and deletes documents
│   ├── help_page.py              # Help page: Provides system usage instructions
├── retriever/                    # Document retrieval and vectorization
│   ├── ingest.py                 # Simulates document vectorization
│   └── loader.py                 # Loads documents for processing
├── chains/                       # Chains for processing data (mock setup for now)
│   └── qa_chain.py               # Simulates a question-answer chain
├── llm/                          # Placeholder for future language model integrations
│   └── __init__.py
├── utils/                        # Utility functions (currently empty)
│   └── __init__.py
└── docs/                         # Directory for user-uploaded documents
```

## Dependencies

- **Gradio**: A Python library for building web UIs. It powers the interface.
- **LangChain**: A framework for developing language model-driven applications. It is used for querying the knowledge base.
- **ChromaDB**: A vector database for storing and searching document vectors.
- **Pandas**: For manipulating data and generating markdown formatted tables.
- **Python-docx**: A library for processing DOCX documents.
- **PyPDF2**: A library for processing PDF documents.

The required libraries are listed in `requirements.txt`, and can be installed with:

```bash
pip install -r requirements.txt
```

## How to Use

### Step 1: Clone the repository

```bash
git clone https://github.com/cyvin/private_qa_bot_optimized.git
cd private_qa_bot_optimized
```

### Step 2: Set up your environment

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Step 3: Configure the environment

Create a `.env` file (if you need to configure API keys, etc.) in the root directory and add necessary configuration details. Example:

```env
DEEPSEEK_API_KEY=your_api_key_here
```

### Step 4: Run the application

Launch the application using:

```bash
python app.py
```

This will start a local server, and you can access the interface in your web browser at:

```
http://localhost:7860
```

## System Components

### 1. **Gradio Interface**

The system is powered by **Gradio**, providing a user-friendly interface with tabs for different functionalities:

- **Q&A Tab**: Users can ask questions, and the system will retrieve relevant answers from the knowledge base.
- **Documents Tab**: Users can upload new documents, which are automatically vectorized and stored.
- **History Tab**: Displays previously asked questions and their answers from the system’s database.
- **Help Tab**: Provides instructions on how to use the system.

### 2. **Document Management**

Documents can be uploaded through the **Documents Tab**. Upon upload, the documents are vectorized using a pre-configured model (defined in `config.py`) and stored in a vector database (Chroma). This allows the system to perform efficient, document-based queries.

### 3. **Q&A Chain**

The **Q&A Chain** uses LangChain to query the knowledge base and retrieve answers. It supports basic question-answering functionality, where questions are answered based on the context of the documents in the knowledge base.

### 4. **SQLite Database**

The **SQLite database** (`chat_history.db`) stores all interactions, including:

- User questions
- Assistant answers
- Timestamps

This data is used for history retrieval and can be managed via the **History Tab**.

## Future Enhancements

1. **Integrate Real Language Models**: Replace the mock `qa_chain` with a real language model like OpenAI’s GPT or Claude from Anthropic.
2. **Multilingual Support**: Extend support to handle multilingual documents and queries.
3. **More Document Formats**: Support additional document formats like Markdown or even images (with OCR).
4. **User Authentication**: Implement user authentication and multi-user capabilities to allow for personal knowledge spaces.
5. **Model Customization**: Provide options for users to customize the embeddings and models used for vectorization.

## Known Issues

- **Performance**: Currently, document vectorization and retrieval are simulated. Integrating with a real model and database like DeepSeek or OpenAI would enhance performance and accuracy.
- **Scalability**: The system is designed for small-scale use. For larger document sets, optimizations for data storage and retrieval will be required.

## Conclusion

This **Private Q&A Bot Optimized** project is a solid base for building a custom knowledge management and question-answering system. It supports document upload, vectorization, and retrieval, making it a useful tool for personal and enterprise-level knowledge bases. Future improvements could focus on integrating with real language models and expanding the document handling capabilities.