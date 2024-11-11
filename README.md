DialoGPT Chatbot

A simple conversational chatbot using Microsoft's DialoGPT and Hugging Face's Transformers library. This chatbot remembers recent conversation history to create a more engaging user experience.
Features

    Conversational Memory: Maintains recent conversation context.
    Truncated Chat History: Limits context to recent exchanges, reducing repetition.

Prerequisites

    Python 3.6+
    Miniconda or Anaconda (recommended for environment management)
    VS Codium (optional, for development environment)

Setup

    Clone the repository (or create a new project folder).

    Create and activate a Conda environment:

conda create -n iris-env python=3.11
conda activate iris-env

Install Required Libraries:

pip install torch transformers

Download the Code: Save dialo_gpt.py (or your main Python script) in the project folder.

Example Usage

After launching, type in your messages to chat with the bot. Type 'exit' to quit.

You: hey
Bot: Hey! :D
You: Can you help me code?
Bot: Sure, I'll help you out!

Code Explanation

    Model and Tokenizer: Loads the microsoft/DialoGPT-medium model and tokenizer.
    Chat History Management: Keeps recent conversation context, limiting it to avoid memory overflow and repetition.
    Response Generation: Bot responds to user input based on conversation history.

File Structure

project_folder/
│
├── dialo_gpt.py           # Main chatbot script
└── README.md               # Project README

dialo_gpt.py

This script includes:

    get_response(): Function to handle user input, generate bot response, and manage conversation history.
