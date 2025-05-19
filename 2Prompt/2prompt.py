# modulos
import os
import requests
from bs4 import BeautifulSoup
from typing import List
from dotenv import load_dotenv
import openai
import google.generativeai as genai
import google.generativeai
import anthropic
import gradio as gr
from gradio import themes

# carrega as chaves de API a partir do arquivo.env

load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')

# Print the key prefixes to help with any debugging

if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")
    
if anthropic_api_key:
    print(f"Anthropic API Key exists and begins {anthropic_api_key[:7]}")
else:
    print("Anthropic API Key not set")

if google_api_key:
    print(f"Google API Key exists and begins {google_api_key[:8]}")
else:
    print("Google API Key not set")

# configura a API do gemini

google.generativeai.configure()

# define o system message de modo global (para gemini)
# system message é a instrução para o modelo

system_message = "You are a helpful assistant that responds in markdown"

# função stream gpt

def stream_gpt(prompt):
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
      ]
    stream = openai.chat.completions.create(
        model='gpt-4o-mini',
        messages=messages,
        stream=True
    )
    result = ""
    for chunk in stream:
        result += chunk.choices[0].delta.content or ""
        yield result

# função stream gemini

def stream_gemini(prompt):
    gemini = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    safety_settings=None,
    system_instruction=system_message
    )

    response = gemini.generate_content(prompt, safety_settings=[
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"}], stream=True)
    
    result = ""
    for chunk in response:
        result += chunk.text
        yield result

# escolha do modelo

#desc = "CHAT GPT e Gemini"

def stream_model(prompt, model):
    if model=="GPT":
        result = stream_gpt(prompt)
    elif model=="Gemini":
        result = stream_gemini(prompt)
    else:
        raise ValueError("Unknown model")
    yield from result

with gr.Blocks(theme=gr.themes.Soft()) as view:
    with gr.Column(elem_id="header", scale=1):
        gr.Markdown(
            """
            <div style='text-align: center; font-size: 24px; font-weight: bold; margin-bottom: 10px'>
                Escolha o modelo 
            </div>
            <div style='text-align: center; font-size: 40px; margin-bottom: 20px'>
                🧠 GPT || 🤖 Gemini
            </div>
            """, 
            elem_id="title"
        )
        gr.Interface(
                fn=stream_model,
                inputs=[gr.Textbox(label="Prompt"), gr.Dropdown(["GPT", "Gemini"], label="Selecione o modelo", value="GPT")],
                outputs=[gr.Textbox(label="Resposta")],
                flagging_mode="never",
                #description=desc,	
                theme=gr.themes.Base(),
                share=True
                #theme=gr.Theme.from_hub('JohnSmith9982/small_and_pretty')
                )
        view.launch()
