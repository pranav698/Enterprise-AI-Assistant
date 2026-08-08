import os
from transformers import AutoTokenizer
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def token_size(input_text):
    # Load the Hugging Face token from the environment variables
    huggingface_token = os.getenv("HF_TOKEN")
    if not huggingface_token:
        raise ValueError("HF_TOKEN not found. Please set it in the environment variables.")

    # Load the pre-trained tokenizer
    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B-Instruct", token=huggingface_token)

    tokenizer.pad_token = tokenizer.eos_token

    tokens = tokenizer.encode(
        input_text,
        add_special_tokens=True,
    )

    return len(tokens) + 40
