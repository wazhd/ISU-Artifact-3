import asyncio
import os
import streamlit as st
from dotenv import load_dotenv
import google.genai as genai
from google.genai import types
from gradio_client import Client
import logic
import json

load_dotenv()

llama_client = True
gemma_client = True

token_1 = os.environ.get("HF_TOKEN")
token_2 = os.environ.get("HF_TOKEN_2")
try:
    llama_client_1 = Client("huggingface-projects/llama-3.2-3B-Instruct", token=token_1)
    llama_client_2 = Client("huggingface-projects/llama-3.2-3B-Instruct", token=token_2)
except Exception as e:
    llama_client = False

try:
    gemma_client_1 = Client("huggingface-projects/gemma-3-12b-it", token=token_1)
    gemma_client_2 = Client("huggingface-projects/gemma-3-12b-it", token=token_2)

except Exception as e:
    gemma_client = False



gemini_api_key_1 = os.environ.get("GEMINI_API_KEY_1")
gemini_api_key_2 = os.environ.get("GEMINI_API_KEY_2")
gemini_api_key_3 = os.environ.get("GEMINI_API_KEY_3")
gemini_api_key_4 = os.environ.get("GEMINI_API_KEY_4")

elevenlabs_api_key_1= os.environ.get("ELEVENLABS_API_KEY_1")
elevenlabs_api_key_2 = os.environ.get("ELEVENLABS_API_KEY_2")

gemini_client_1 = genai.Client(api_key=gemini_api_key_1)
gemini_client_2 = genai.Client(api_key=gemini_api_key_2)
gemini_client_3 = genai.Client(api_key=gemini_api_key_3)
gemini_client_4 = genai.Client(api_key=gemini_api_key_4)


with open("life_advice_ai_instructions.txt", "r") as f:
    instructions = f.read()

async def generate_response(user_input, history):
    data_2 = logic.read_save()
    data = json.dumps(data_2, indent=2)

    gemini_instructions = instructions + "\n\n Life Data: \n\n" + data + "\n\n Chat History: " + history
    llama_instructions = f"{instructions} \n\n Life Data: {data} \n\n Chat History: {history}. User says: {user_input}"
    gemma_instructions = f"{instructions} + \n\n Life Data: {data} \n\n Chat History: {history}"

    if st.session_state.ai_model == "gemini_1":
        try:
            config = types.GenerateContentConfig(
                system_instruction=gemini_instructions, temperature=0.7)
            chat = gemini_client_1.aio.chats.create(model="gemini-3-flash-preview", config=config)
            response = await chat.send_message(user_input)
            return response.text
        except Exception as e:
            st.session_state.ai_model = "gemini_2"
    if st.session_state.ai_model == "gemini_2":

        try:

            config = types.GenerateContentConfig(

                system_instruction=gemini_instructions, temperature = 0.7)
            chat = gemini_client_2.aio.chats.create(model="gemini-3-flash-preview", config=config)

            response = await chat.send_message(user_input)

            return response.text

        except Exception as e:
            st.session_state.ai_model = "gemini_3"
    if st.session_state.ai_model == "gemini_3":

        try:

            config = types.GenerateContentConfig(

                system_instruction=gemini_instructions, temperature = 0.7)

            chat = gemini_client_3.aio.chats.create(model="gemini-3-flash-preview", config=config)

            response = await chat.send_message(user_input)

            return response.text

        except Exception as e:

            st.session_state.ai_model = "gemini_4"
    if st.session_state.ai_model == "gemini_4":
        try:

            config = types.GenerateContentConfig(

                system_instruction=gemini_instructions, temperature = 0.7)

            chat = gemini_client_4.aio.chats.create(model="gemini-3-flash-preview", config=config)

            response = await chat.send_message(user_input)

            return response.text

        except Exception as e:
            st.session_state.ai_model = "llama_1"

    if llama_client:
        if st.session_state.ai_model == "llama_1":
            try:
                result = await asyncio.to_thread(
                    llama_client_1.predict,
                    message=llama_instructions,
                    max_new_tokens=1024,
                    temperature=0.7,
                    top_p=0.9,
                    top_k=50,
                    repetition_penalty=1.2,
                    api_name="/generate"
                )
                return result
            except Exception as e:
                st.session_state.ai_model = "llama_2"


        if st.session_state.ai_model == "llama_2":
            try:
                result = await asyncio.to_thread(
                    llama_client_2.predict,
                    message=llama_instructions,
                    max_new_tokens=1024,
                    temperature=0.7,
                    top_p=0.9,
                    top_k=50,
                    repetition_penalty=1.2,
                    api_name="/generate"
                )
                return result
            except Exception as e:
                st.session_state.ai_model = "gemma_1"
    if gemma_client:
        if st.session_state.ai_model == "gemma_1":
            try:
                result = await asyncio.to_thread(
                    gemma_client_1.predict,
                    message={"text": user_input, "files": []},
                    system_prompt=gemma_instructions,
                    max_new_tokens=700,
                    api_name="/run"
                )

                return result
            except Exception as e:
                st.session_state.ai_model = "gemma_2"

        if st.session_state.ai_model == "gemma_2":
            try:
                result = await asyncio.to_thread(
                    gemma_client_2.predict,
                    message={"text": user_input, "files": []},
                    system_prompt=gemma_instructions,
                    max_new_tokens=700,
                    api_name="/run"
                )
                return result
            except Exception as e:
                return "Sorry something went wrong"