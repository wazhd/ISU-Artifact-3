import streamlit as st
import ai
import asyncio
import logic
import pandas as pd

st.set_page_config(initial_sidebar_state="collapsed", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "menu"

if st.session_state.page == "menu":
    left, middle, right = st.columns([1, 2, 1])

    with middle:
        st.title("Life Simulator")
        st.write("")
        st.write("")
        if st.button("Play", use_container_width=True):
            st.session_state.page = "create"
            st.rerun()

elif st.session_state.page == "create":
    st.title("Life Simulator")
    left, right = st.columns([1, 1])

    with left:
        with st.container(border=True):
            if st.button("Create new life", use_container_width=True):
                st.session_state.page = "signup"
                st.rerun()

    with right:
        with st.container(border=True):
            if st.button("Enter existing life", use_container_width=True):
                st.session_state.page = "login"
                st.rerun()

elif st.session_state.page == "login":
    left, middle, right = st.columns([1, 2, 1])

    with middle:
        st.title("Enter existing life")
        with st.container(border=True):
            name = st.text_input("Name", key="log_name")
            id_val = st.text_input("ID", type="password", key="log_id")

            if st.button("Enter existing life", use_container_width=True):
                current_data = logic.read_pkl()

                if name not in current_data:
                    st.error("Name doesn't exist")
                elif current_data[name].get("password") != id_val:
                    st.error("Incorrect password")
                else:
                    st.session_state.name = name
                    st.session_state.page = "home"
                    st.rerun()

        if st.button("Return"):
            st.session_state.page = "menu"
            st.rerun()

elif st.session_state.page == "signup":
    left, middle, right = st.columns([1, 2, 1])

    with middle:
        st.title("Create New Life")
        with st.container(border=True):
            name = st.text_input("Name", key="reg_name")
            id_val = st.text_input("ID", type="password", key="reg_id")

            if st.button("Start new life", use_container_width=True):
                current_data = logic.read_pkl()

                if name in current_data:
                    st.error("Name taken!")
                elif name == "" or id_val == "":
                    st.warning("Fill all fields")
                else:
                    logic.resetAll(name, id_val)
                    st.session_state.name = name
                    st.session_state.page = "home"
                    st.rerun()

        if st.button("Return"):
            st.session_state.page = "menu"
            st.rerun()

elif st.session_state.page == "home":
    st.title("Manage Your Life")
    st.write("")
    st.write("")

    left, middle, right = st.columns([1, 1, 1])
    with left:
        with st.container(border=True):
            st.image("assets/bank.png")
            if st.button("Bank", use_container_width=True):
                st.session_state.page = "bank"
                st.rerun()
        with st.container(border=True):
            st.image("assets/budget.png")
            if st.button("Budget", use_container_width=True):
                st.session_state.page = "budget"
                st.rerun()

    with middle:
        with st.container(border=True):
            st.image("assets/stock.png")
            if st.button("Stock Market", use_container_width=True):
                st.session_state.page = "stock"
                st.rerun()

elif st.session_state.page == "stock":
    st.subheader("Stock Market Simulation")

    user_name = st.session_state.name

    h1 = logic.get3(user_name, "stocks", "Dave and Son's Coal Mine", "price_history")
    h2 = logic.get3(user_name, "stocks", "Xavier's Egg Farm", "price_history")
    h3 = logic.get3(user_name, "stocks", "Mr. Fox's Chicken Company", "price_history")
    h4 = logic.get3(user_name, "stocks", "Raymond's Water Company", "price_history")

    st.write("Market Trends")
    chart_data = {
        "Coal Mine": h1,
        "Egg Farm": h2,
        "Chicken Co": h3,
        "Water Co": h4
    }
    st.line_chart(chart_data)

    if st.button("Advance Month"):
        asyncio.run(ai.simulate_stock(user_name))
        st.rerun()

    st.divider()

    stock_options = [
        "Dave and Son's Coal Mine", "Xavier's Egg Farm",
        "Mr. Fox's Chicken Company", "Raymond's Water Company"
    ]

    display_name = st.selectbox("Select a stock to trade", stock_options)

    current_money = logic.get2(user_name, "bank", "money")
    shares_owned = logic.get3(user_name, "stocks", display_name, "owned")

    raw_price = logic.get3(user_name, "stocks", display_name, "price")
    current_price = float(raw_price) if raw_price not in ["", 0] else 0.0

    st.write(f"Balance: ${current_money:,.2f} | Shares Owned: {shares_owned}")
    st.write(f"Current Price: **${current_price:,.2f}**")

    col1, col2 = st.columns(2)

    with col1:
        buy_qty = st.number_input("Buy Amount", min_value=0, step=1, key="buy_btn")
        if st.button("Buy") and buy_qty > 0:
            total_cost = buy_qty * current_price
            if total_cost <= current_money:
                logic.update2(user_name, "bank", "money", current_money - total_cost)
                logic.update3(user_name, "stocks", display_name, "owned", shares_owned + buy_qty)
                st.rerun()
            else:
                st.error("Not enough money!")

    with col2:
        sell_qty = st.number_input("Sell Amount", min_value=0, step=1, key="sell_btn")
        if st.button("Sell") and sell_qty > 0:
            if sell_qty <= shares_owned:
                total_gain = sell_qty * current_price
                logic.update2(user_name, "bank", "money", current_money + total_gain)
                logic.update3(user_name, "stocks", display_name, "owned", shares_owned - sell_qty)
                st.rerun()
            else:
                st.error("Not enough shares!")

    if st.button("Back to Home"):
        st.session_state.page = "home"
        st.rerun()