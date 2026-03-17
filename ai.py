import google.genai as genai
from dotenv import load_dotenv
from gradio_client import Client
import asyncio
from google.genai import types
import os
import streamlit as st
import logic
import re

load_dotenv()

llama_client = True
gemma_client = True

token_1 = os.environ.get("HF_TOKEN")
token_2 = os.environ.get("HF_TOKEN_2")

if "ai_model" not in st.session_state:
    st.session_state.ai_model = "gemini_1"

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

with open("stock_ai_instructions.txt", "r") as f:
    instructions = f.read()


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

async def simulate_stock(name):

    data = logic.read_pkl()

    stock_data = data["stocks"]

    if st.session_state.ai_model == "gemini_1":
        try:
            config = types.GenerateContentConfig(
                system_instruction="REMEMBER THESE INSTRUCTIONS VERY CAREFULLY: \n\n" + instructions + "\n\n" + "Stock history: " + stock_data, temperature=0)
            chat = gemini_client_1.aio.chats.create(model="gemini-3-flash-preview", config=config)
            response = await chat.send_message("REMEMBER THESE INSTRUCTIONS VERY CAREFULLY: \n\n" + instructions + "\n\n" + "Stock history: " + stock_data)
            values = response.text
            get_value(name, values)
        except Exception as e:
            st.session_state.ai_model = "gemini_2"
    elif st.session_state.ai_model == "gemini_2":

        try:

            config = types.GenerateContentConfig(

                system_instruction="REMEMBER THESE INSTRUCTIONS VERY CAREFULLY: \n\n" + instructions + "\n\n" + "Stock history: " + stock_data, temperature=0)

            chat = gemini_client_2.aio.chats.create(model="gemini-3-flash-preview", config=config)

            response = await chat.send_message("REMEMBER THESE INSTRUCTIONS VERY CAREFULLY: \n\n" + instructions + "\n\n" + "Stock history: " + stock_data)
            values = response.text

            get_value(name, values)

        except Exception as e:
            st.session_state.ai_model = "gemini_3"
    elif st.session_state.ai_model == "gemini_3":

        try:

            config = types.GenerateContentConfig(

                system_instruction="REMEMBER THESE INSTRUCTIONS VERY CAREFULLY: \n\n" + instructions + "\n\n" + "Stock history: " + stock_data, temperature=0)

            chat = gemini_client_3.aio.chats.create(model="gemini-3-flash-preview", config=config)

            response = await chat.send_message("REMEMBER THESE INSTRUCTIONS VERY CAREFULLY: \n\n" + instructions + "\n\n" + "Stock history: " + stock_data)
            values = response.text

            get_value(name, values)

        except Exception as e:

            st.session_state.ai_model = "gemini_4"
    elif st.session_state.ai_model == "gemini_4":
        try:

            config = types.GenerateContentConfig(

                system_instruction="REMEMBER THESE INSTRUCTIONS VERY CAREFULLY: \n\n" + instructions + "\n\n" + "Stock history: " + stock_data, temperature=0)

            chat = gemini_client_4.aio.chats.create(model="gemini-3-flash-preview", config=config)

            response = await chat.send_message("REMEMBER THESE INSTRUCTIONS VERY CAREFULLY: \n\n" + instructions + "\n\n" + "Stock history: " + stock_data)
            values = response.text

            get_value(name, values)

        except Exception as e:
            st.session_state.ai_model = "llama_1"

    elif llama_client:
        if st.session_state.ai_model == "llama_1":
            try:
                result = await asyncio.to_thread(
                    llama_client_1.predict,
                    message="REMEMBER THESE INSTRUCTIONS VERY CAREFULLY: \n\n" + instructions + "\n\n" + "Stock history: " + stock_data,
                    max_new_tokens=1024,
                    temperature=0,
                    top_p=0.9,
                    top_k=50,
                    repetition_penalty=1.2,
                    api_name="/generate"
                )
                values = result

                get_value(name, values)
            except Exception as e:
                st.session_state.ai_model = "llama_2"


        elif st.session_state.ai_model == "llama_2":
            try:
                result = await asyncio.to_thread(
                    llama_client_2.predict,
                    message="REMEMBER THESE INSTRUCTIONS VERY CAREFULLY: \n\n" + instructions + "\n\n" + "Stock history: " + stock_data,
                    max_new_tokens=1024,
                    temperature=0,
                    top_p=0.9,
                    top_k=50,
                    repetition_penalty=1.2,
                    api_name="/generate"
                )
                values = result

                get_value(name, values)
            except Exception as e:
                st.session_state.ai_model = "gemma_1"
    elif gemma_client:
        if st.session_state.ai_model == "gemma_1":
            try:
                result = await asyncio.to_thread(
                    gemma_client_1.predict,
                    message={"text": "REMEMBER THESE INSTRUCTIONS VERY CAREFULLY: \n\n" + instructions + "\n\n" + "Stock history: " + stock_data, "files": []},
                    system_prompt="REMEMBER THESE INSTRUCTIONS VERY CAREFULLY: \n\n" + instructions + "\n\n" + "Stock history: " + stock_data,
                    max_new_tokens=700,
                    api_name="/run"
                )
                values = result

                get_value(name, values)
            except Exception as e:
                st.session_state.ai_model = "gemma_2"

        elif st.session_state.ai_model == "gemma_2":
            try:
                result = await asyncio.to_thread(
                    gemma_client_2.predict,
                    message={"text": "REMEMBER THESE INSTRUCTIONS VERY CAREFULLY: \n\n" + instructions + "\n\n" + "Stock history: " + stock_data, "files": []},
                    system_prompt="REMEMBER THESE INSTRUCTIONS VERY CAREFULLY: \n\n" + instructions + "\n\n" + "Stock history: " + stock_data,
                    max_new_tokens=700,
                    api_name="/run"
                )
                values = result

                get_value(name, values)
            except Exception as e:
                st.error("Cannot generate stocks right now")


def get_value(name, values):
    stocks = re.findall(r'-?\d+\.?\d*', values)

    logic.update3(name, "stocks", "Dave and Son's Coal Mine", "price", stocks[0])
    stock1_history = logic.get3(name, "stocks", "Dave and Son's Coal Mine", "price_history")
    stock1_history.append(float(stocks[0]))
    logic.update3(name, "stocks", "Dave and Son's Coal Mine", "price_history", stock1_history)

    logic.update3(name, "stocks", "Xavier's Egg Farm", "price", stocks[1])
    stock2_history = logic.get3(name, "stocks", "Xavier's Egg Farm", "price_history")
    stock2_history.append(float(stocks[1]))
    logic.update3(name, "stocks", "Xavier's Egg Farm", "price_history", stock2_history)

    logic.update3(name, "stocks", "Mr. Fox's Chicken Company", "price", stocks[2])
    stock3_history = logic.get3(name, "stocks", "Mr. Fox's Chicken Company", "price_history")
    stock3_history.append(float(stocks[2]))
    logic.update3(name, "stocks", "Mr. Fox's Chicken Company", "price_history", stock3_history)

    logic.update3(name, "stocks", "Raymond's Water Company", "price", stocks[3])
    stock4_history = logic.get3(name, "stocks", "Raymond's Water Company", "price_history")
    stock4_history.append(float(stocks[3]))
    logic.update3(name, "stocks", "Raymond's Water Company", "price_history", stock4_history)