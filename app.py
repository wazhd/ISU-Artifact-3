import streamlit as st
import logic
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

st.set_page_config(initial_sidebar_state="collapsed", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "menu"
    logic.save(logic.starting_stats)

if st.session_state.page == "menu":
    left, middle, right = st.columns([1, 2, 1])
    with middle:
        st.title("Life Simulator")
        if st.button("Play", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()

elif st.session_state.page == "home":
    st.title("Manage Your Life")
    data = logic.read_save()
    logic.empty(2)

    st.markdown(f"#### **Total Money:** ${data['money']:.2f}")
    if "job" not in data:
        st.markdown(f"#### **Job:** none")
    else:
        st.markdown(f"#### **Job:** {data['job']}")

    st.markdown(f"#### **Monthly Gross Income:** ${data['gross income']:.2f}")
    st.markdown(f"#### **Monthly Net Income:** ${data['net income']:.2f}")
    st.markdown(f"#### **Month:** {data['month']}")

    logic.empty(2)

    if st.button("+1 Month", use_container_width=True):
        logic.update_simulation()
        st.rerun()

    st.divider()

    logic.empty(2)

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

        with st.container(border=True):
            st.image("assets/assets.png")
            if st.button("Assets", use_container_width=True):
                st.session_state.page = "assets"
                st.rerun()
    with right:
        with st.container(border=True):
            st.image("assets/job.png")
            if st.button("Find a job", use_container_width=True):
                st.session_state.page = "job"
                st.rerun()
elif st.session_state.page == "stock":
    data = logic.read_save()
    st.title("Stock Market")

    stock_options = list(data["stocks"].keys())
    display_name = st.selectbox("Select a stock to analyse", stock_options)

    graph, panel = st.columns([3, 1])

    current_price = data["stocks"][display_name]["price"]
    current_money = data["money"]
    stock_number = data["stocks"][display_name]["owned"]
    history = data["stocks"][display_name]["price_history"]

    with graph:
        st.write("")
        st.write("")

        fig, ax = plt.subplots(figsize=(10, 5))
        months = list(range(len(history)))
        ax.plot(months, history, marker='o', linestyle='-', color='#1f77b4')
        max_month = max(1, len(history) - 1)
        ax.set_xlim(left=-0.5, right=max_month + 0.5)
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.set_title(display_name)
        ax.set_xlabel("Months")
        ax.set_ylabel("Price ($)")
        ax.grid(True, alpha=0.3)

        st.pyplot(fig)

        st.divider()


    with panel:
        st.write("### Stats")
        st.metric("Current Price", f"${current_price:,.2f}")
        st.write(f"**Current Shares:** {stock_number}")
        st.write(f"**Current Balance:** ${current_money:,.2f}")
        if len(history) >= 2:
            change = ((current_price - history[-2]) / history[-2]) * 100
            if change > 0:
                st.write(f"**Appreciated** by {change:.2f}% since last month")
            else:
                st.write(f"**Declined** by {-change:.2f}% since last month")

        rate = logic.calculate_average_monthly_change(history)

        if rate > 0:
             st.write(f"**Average Appreciation Rate:** {logic.calculate_average_monthly_change(history)}% per month")
        else:
            st.write(f"**Average Depreciation Rate:** {logic.calculate_average_monthly_change(history)}% per month")

        st.divider()

        buy_input = st.number_input("Buy shares", min_value=0, step=1)
        if buy_input > 0:
            total_cost = current_price * buy_input
            balance_after = current_money - total_cost
            shares_after = stock_number + buy_input

            st.write(f"Shares After: {shares_after:,.2f}")
            st.write(f"Cost: ${total_cost:,.2f}")
            st.write(f"Balance After: ${balance_after:,.2f}")

            if total_cost > current_money:
                st.error("Insufficient funds!")
            else:
                if st.button("Confirm Purchase", use_container_width=True):
                    data["money"] = balance_after
                    data["stocks"][display_name]["owned"] = shares_after
                    logic.save(data)
                    st.rerun()

        st.divider()

        sell_input = st.number_input("Sell shares", min_value=0, step=1)
        if sell_input > 0:
            if sell_input > stock_number:
                st.error("Not enough shares!")
            else:
                gain = sell_input * current_price
                balance_after = current_money + gain
                shares_after = stock_number - sell_input

                st.write(f"Shares After: {shares_after:,.2f}")
                st.write(f"Earnings: ${gain:,.2f}")
                st.write(f"Balance After: ${balance_after:,.2f}")

                if st.button("Confirm Sale", use_container_width=True):
                    data["money"] = balance_after
                    data["stocks"][display_name]["owned"] = shares_after
                    logic.save(data)
                    st.rerun()
    if st.button("Back", use_container_width=False):
        st.session_state.page = "home"
        st.rerun()

elif st.session_state.page == "job":
    data = logic.read_save()
    job_data = data["jobs"]
    st.title("Choose a Job")

    with st.container(border=True):
        st.markdown("# Farmer")
        st.markdown(f"#### **Monthly Salary:** ${job_data['farmer']['gross income']:,.2f}")
        st.markdown(f"#### **Monthly Gross Income:** ${job_data['farmer']['gross income']:,.2f}")
        st.markdown(f"#### **Monthly Net Income:** ${job_data['farmer']['net income']:,.2f}")
        st.markdown(
            f"#### **Difference:** ${job_data['farmer']['gross income'] - job_data['farmer']['net income']:,.2f}")
        st.markdown(
            f"#### **Tax Rate:** {logic.calculate_change(job_data['farmer']['gross income'], job_data['farmer']['net income'])}%")
        logic.empty(1)
        if data.get("job") != "farmer":
            if st.button("Get this job!", key="btn_farmer"):
                data["job"] = "farmer"
                data["gross income"] = job_data["farmer"]["gross income"]
                data["net income"] = job_data["farmer"]["net income"]
                logic.save(data)
                st.rerun()
        else:
            st.button("You already have this job", key="has_farmer", disabled=True)

    with st.container(border=True):
        st.markdown("# Librarian")
        st.markdown(f"#### **Monthly Salary:** ${job_data['librarian']['gross income']:,.2f}")
        st.markdown(f"#### **Monthly Gross Income:** ${job_data['librarian']['gross income']:,.2f}")
        st.markdown(f"#### **Monthly Net Income:** ${job_data['librarian']['net income']:,.2f}")
        st.markdown(
            f"#### **Difference:** ${job_data['librarian']['gross income'] - job_data['librarian']['net income']:,.2f}")
        st.markdown(
            f"#### **Tax Rate:** {logic.calculate_change(job_data['librarian']['gross income'], job_data['librarian']['net income'])}%")
        logic.empty(1)
        if data.get("job") != "librarian":
            if st.button("Get this job!", key="btn_librarian"):
                data["job"] = "librarian"
                data["gross income"] = job_data["librarian"]["gross income"]
                data["net income"] = job_data["librarian"]["net income"]
                logic.save(data)
                st.rerun()
        else:
            st.button("You already have this job", key="has_librarian", disabled=True)

    with st.container(border=True):
        st.markdown("# Plumber")
        st.markdown(f"#### **Monthly Salary:** ${job_data['plumber']['gross income']:,.2f}")
        st.markdown(f"#### **Monthly Gross Income:** ${job_data['plumber']['gross income']:,.2f}")
        st.markdown(f"#### **Monthly Net Income:** ${job_data['plumber']['net income']:,.2f}")
        st.markdown(
            f"#### **Difference:** ${job_data['plumber']['gross income'] - job_data['plumber']['net income']:,.2f}")
        st.markdown(
            f"#### **Tax Rate:** {logic.calculate_change(job_data['plumber']['gross income'], job_data['plumber']['net income'])}%")
        logic.empty(1)
        if data.get("job") != "plumber":
            if st.button("Get this job!", key="btn_plumber"):
                data["job"] = "plumber"
                data["gross income"] = job_data["plumber"]["gross income"]
                data["net income"] = job_data["plumber"]["net income"]
                logic.save(data)
                st.rerun()
        else:
            st.button("You already have this job", key="has_plumber", disabled=True)

    with st.container(border=True):
        st.markdown("# Electrician")
        st.markdown(f"#### **Monthly Salary:** ${job_data['electrician']['gross income']:,.2f}")
        st.markdown(f"#### **Monthly Gross Income:** ${job_data['electrician']['gross income']:,.2f}")
        st.markdown(f"#### **Monthly Net Income:** ${job_data['electrician']['net income']:,.2f}")
        st.markdown(
            f"#### **Difference:** ${job_data['electrician']['gross income'] - job_data['electrician']['net income']:,.2f}")
        st.markdown(
            f"#### **Tax Rate:** {logic.calculate_change(job_data['electrician']['gross income'], job_data['electrician']['net income'])}%")
        logic.empty(1)
        if data.get("job") != "electrician":
            if st.button("Get this job!", key="btn_electrician"):
                data["job"] = "electrician"
                data["gross income"] = job_data["electrician"]["gross income"]
                data["net income"] = job_data["electrician"]["net income"]
                logic.save(data)
                st.rerun()
        else:
            st.button("You already have this job", key="has_electrician", disabled=True)

    with st.container(border=True):
        st.markdown("# Pharmacist")
        st.markdown(f"#### **Monthly Salary:** ${job_data['pharmacist']['gross income']:,.2f}")
        st.markdown(f"#### **Monthly Gross Income:** ${job_data['pharmacist']['gross income']:,.2f}")
        st.markdown(f"#### **Monthly Net Income:** ${job_data['pharmacist']['net income']:,.2f}")
        st.markdown(
            f"#### **Difference:** ${job_data['pharmacist']['gross income'] - job_data['pharmacist']['net income']:,.2f}")
        st.markdown(
            f"#### **Tax Rate:** {logic.calculate_change(job_data['pharmacist']['gross income'], job_data['pharmacist']['net income'])}%")
        logic.empty(1)
        if data.get("job") != "pharmacist":
            if st.button("Get this job!", key="btn_pharmacist"):
                data["job"] = "pharmacist"
                data["gross income"] = job_data["pharmacist"]["gross income"]
                data["net income"] = job_data["pharmacist"]["net income"]
                logic.save(data)
                st.rerun()
        else:
            st.button("You already have this job", key="has_pharmacist", disabled=True)

    with st.container(border=True):
        st.markdown("# Cashier")
        st.markdown(f"#### **Monthly Salary:** ${job_data['cashier']['gross income']:,.2f}")
        st.markdown(f"#### **Monthly Gross Income:** ${job_data['cashier']['gross income']:,.2f}")
        st.markdown(f"#### **Monthly Net Income:** ${job_data['cashier']['net income']:,.2f}")
        st.markdown(
            f"#### **Difference:** ${job_data['cashier']['gross income'] - job_data['cashier']['net income']:,.2f}")
        st.markdown(
            f"#### **Tax Rate:** {logic.calculate_change(job_data['cashier']['gross income'], job_data['cashier']['net income'])}%")
        logic.empty(1)
        if data.get("job") != "cashier":
            if st.button("Get this job!", key="btn_cashier"):
                data["job"] = "cashier"
                data["gross income"] = job_data["cashier"]["gross income"]
                data["net income"] = job_data["cashier"]["net income"]
                logic.save(data)
                st.rerun()
        else:
            st.button("You already have this job", key="has_cashier", disabled=True)

    with st.container(border=True):
        st.markdown("# Construction Worker")
        st.markdown(f"#### **Monthly Salary:** ${job_data['construction worker']['gross income']:,.2f}")
        st.markdown(f"#### **Monthly Gross Income:** ${job_data['construction worker']['gross income']:,.2f}")
        st.markdown(f"#### **Monthly Net Income:** ${job_data['construction worker']['net income']:,.2f}")
        st.markdown(
            f"#### **Difference:** ${job_data['construction worker']['gross income'] - job_data['construction worker']['net income']:,.2f}")
        st.markdown(
            f"#### **Tax Rate:** {logic.calculate_change(job_data['construction worker']['gross income'], job_data['construction worker']['net income'])}%")
        logic.empty(1)
        if data.get("job") != "construction worker":
            if st.button("Get this job!", key="btn_construction"):
                data["job"] = "construction worker"
                data["gross income"] = job_data["construction worker"]["gross income"]
                data["net income"] = job_data["construction worker"]["net income"]
                logic.save(data)
                st.rerun()
        else:
            st.button("You already have this job", key="has_construction", disabled=True)

    logic.back_button()

elif st.session_state.page == "assets":
    data = logic.read_save()
    asset_data = data["assets"]
    st.title("Assets")
    left, right = st.columns([1,1])
    with left:
        with st.container(border=True):
            st.subheader("Computer")
            if st.button("Buy computers"):
                st.session_state.page = "computer"
                st.rerun()
        with st.container(border=True):
            st.subheader("House")
            if st.button("Buy houses"):
                st.session_state.page = "house"
                st.rerun()

    with right:
        with st.container(border=True):
            st.subheader("Car")
            if st.button("Buy cars"):
                st.session_state.page = "car"
                st.rerun()

        with st.container(border=True):
            st.subheader("Art")
            if st.button("Buy artwork"):
                st.session_state.page = "artwork"
                st.rerun()


    logic.back_button()

elif st.session_state.page == "computer":
    data = logic.read_save()
    computer_data = data["assets"]["computers"]
    st.title("Computers")
    st.markdown(f"### Total Money: ${data['money']:.2f}")

    comp_list = [
        ("Microsoft Laptop", "microsoft laptop"),
        ("MacBook", "macbook"),
        ("Chromebook", "chromebook")
    ]

    for display_name, comp_key in comp_list:
        history = computer_data[comp_key]['history']
        owned_count = computer_data[comp_key]['owned']
        current_price = history[-1]
        current_money = data['money']

        last_entry = history[-1]
        second_last_entry = history[-2] if len(history) > 1 else last_entry

        with st.container(border=True):
            st.subheader(display_name)
            left, right = st.columns([1, 1])

            with left:
                st.markdown(f"#### Price: ${last_entry:,.2f}")
                st.markdown(f"#### Owned: {owned_count}")
                st.markdown(f"#### Depreciated by ${abs(last_entry - second_last_entry):.2f} since last month")
                st.markdown(
                    f"#### Depreciated by {abs(logic.calculate_change(last_entry, second_last_entry)):.2f}% since last month")
                st.markdown(
                    f"#### Average Depreciation Rate: {abs(logic.calculate_average_monthly_change(history)):.2f}% per month")

                st.divider()

                buy_val = st.number_input(f"Buy amount", min_value=0, step=1, key=f"buy_in_{comp_key}")
                if buy_val > 0:
                    cost = current_price * buy_val
                    balance_after = current_money - cost

                    st.write(f"Balance Before: ${current_money:,.2f}")
                    st.write(f"Total Cost: ${cost:,.2f}")
                    st.write(f"Balance After: ${balance_after:,.2f}")

                    if cost > current_money:
                        st.error("Insufficient funds!")
                    else:
                        if st.button(f"Confirm Purchase", key=f"buy_btn_{comp_key}", use_container_width=True):
                            data["money"] = balance_after
                            data["assets"]["computers"][comp_key]["owned"] += buy_val
                            logic.save(data)
                            st.rerun()

                st.divider()

                sell_val = st.number_input(f"Sell amount", min_value=0, step=1, key=f"sell_in_{comp_key}")
                if sell_val > 0:
                    if sell_val > owned_count:
                        st.error("Not enough units!")
                    else:
                        gain = sell_val * current_price
                        balance_after = current_money + gain

                        st.write(f"Balance Before: ${current_money:,.2f}")
                        st.write(f"Total Earnings: ${gain:,.2f}")
                        st.write(f"Balance After: ${balance_after:,.2f}")

                        if st.button(f"Confirm Sale", key=f"sell_btn_{comp_key}", use_container_width=True):
                            data["money"] = balance_after
                            data["assets"]["computers"][comp_key]["owned"] -= sell_val
                            logic.save(data)
                            st.rerun()

            with right:
                fig, ax = plt.subplots(figsize=(10, 6))
                x_vals = list(range(len(history)))
                ax.plot(x_vals, history, marker='o', linestyle='-', color='#1f77b4')
                max_m = max(1, len(history) - 1)
                ax.set_xlim(left=-0.5, right=max_m + 0.5)
                ax.xaxis.set_major_locator(MaxNLocator(integer=True))
                ax.set_title(f"{display_name} Market Value")
                ax.set_xlabel("Months")
                ax.set_ylabel("Price ($)")
                ax.grid(True, alpha=0.3)
                st.pyplot(fig)

    if st.button("Back"):
        st.session_state.page = "assets"
        st.rerun()
