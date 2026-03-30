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


    total_monthly_mortgage = 0
    total_monthly_interest = 0
    for h_key in data["assets"]["houses"]:
        h = data["assets"]["houses"][h_key]
        if h.get("mortgage_active"):
            total_monthly_mortgage += h.get("monthly_payment", 0)
            total_monthly_interest += h.get("monthly_interest_paid", 0)

    st.markdown(f"#### **Total Money:** ${data['money']:.2f}")
    if "job" not in data:
        st.markdown(f"#### **Job:** none")
    else:
        st.markdown(f"#### **Job:** {data['job']}")

    st.markdown(f"#### **Monthly Gross Income:** ${data['gross income']:.2f}")
    st.markdown(f"#### **Monthly Net Income:** ${data['net income']:.2f}")

    st.markdown(f"#### **Monthly Mortgage Paid:** ${total_monthly_mortgage:.2f}")
    st.markdown(f"#### **Monthly Interest Paid:** ${total_monthly_interest:.2f}")

    st.markdown(f"#### ")
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
            st.image("assets/assets.png")
            if st.button("Assets", use_container_width=True):
                st.session_state.page = "assets"
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

elif st.session_state.page == "house":
    data = logic.read_save()
    house_data = data["assets"]["houses"]
    st.title("Houses")
    st.markdown(f"### Total Money: ${data['money']:,.2f}")

    comp_list = [
        ("Single", "single"),
        ("Townhouse", "townhouse"),
        ("Apartment", "apartment")
    ]

    for display_name, comp_key in comp_list:
        h_stats = house_data[comp_key]
        history = h_stats['history']
        owned_count = h_stats['owned']
        current_money = data['money']

        last_entry = history[-1]
        second_last_entry = history[-2] if len(history) > 1 else last_entry

        with st.container(border=True):
            st.subheader(display_name)
            left, right = st.columns([1, 1])

            with left:
                st.markdown(f"#### Price: ${last_entry:,.2f}")
                st.markdown(f"#### Owned: {owned_count}")

                difference = last_entry - second_last_entry
                perc_change = logic.calculate_change(last_entry, second_last_entry)
                avg_rate = logic.calculate_average_monthly_change(history)

                if difference < 0:
                    st.markdown(f"#### Depreciated by ${abs(difference):,.2f} since last month")
                    st.markdown(f"#### Depreciated by {abs(perc_change):.2f}% since last month")
                    st.markdown(f"#### Average Depreciation Rate: {abs(avg_rate):.2f}% per month")
                else:
                    st.markdown(f"#### Appreciated by ${abs(difference):,.2f} since last month")
                    st.markdown(f"#### Appreciated by {abs(perc_change):.2f}% since last month")
                    st.markdown(f"#### Average Appreciation Rate: {abs(avg_rate):.2f}% per month")

                st.divider()

                if h_stats.get("mortgage_active"):
                    st.markdown(f"**Active Mortgage Info:**")
                    st.write(f"Monthly Payment: ${h_stats['monthly_payment']:,.2f}")
                    st.write(f"Interest Paid: ${h_stats.get('monthly_interest_paid', 0):,.2f}")
                    st.write(f"Months Remaining: {h_stats['remaining_months']}")
                    st.divider()

                pay_method = st.radio("Payment Method", ["Cash", "Mortgage"], key=f"meth_{comp_key}")

                if pay_method == "Cash":
                    if st.button(f"Buy using cash", key=f"btn_c_{comp_key}", use_container_width=True):
                        if current_money >= last_entry:
                            data["money"] -= last_entry
                            data["assets"]["houses"][comp_key]["owned"] += 1
                            logic.save(data)
                            st.rerun()
                        else:
                            st.error("Insufficient Funds")
                else:
                    d_pay = st.number_input("Downpayment ($)", 0.0, float(last_entry), last_entry * 0.2,
                                            key=f"down_{comp_key}")
                    m_type = st.selectbox("Interest Type", ["simple", "compound"], key=f"type_{comp_key}")
                    m_rate = st.number_input("Monthly Interest Rate (%)", 0.0, 5.0, 0.5, key=f"rate_{comp_key}")
                    m_months = st.number_input("Months", 1, 360, 180, key=f"dur_{comp_key}")

                    loan_principal = last_entry - d_pay
                    monthly_total = logic.get_monthly_installment(loan_principal, m_rate, m_months, m_type)

                    if m_type == "simple":
                        total_int = logic.calculate_simple_interest(loan_principal, m_rate, m_months)
                    else:
                        total_int = logic.calculate_compound_interest(loan_principal, m_rate, m_months)
                    monthly_interest_paid = total_int / m_months

                    st.write(f"**Monthly Payment:** ${monthly_total:,.2f}")
                    st.write(f"**Monthly Interest Paid:** ${monthly_interest_paid:,.2f}")
                    st.write(f"**Monthly Interest Rate:** {m_rate}%")

                    if st.button(f"Take Mortgage", key=f"btn_m_{comp_key}", use_container_width=True):
                        if current_money >= d_pay:
                            data["money"] -= d_pay
                            data["assets"]["houses"][comp_key]["owned"] += 1
                            data["assets"]["houses"][comp_key]["mortgage_active"] = True
                            data["assets"]["houses"][comp_key]["monthly_payment"] = monthly_total
                            data["assets"]["houses"][comp_key]["monthly_interest_paid"] = monthly_interest_paid
                            data["assets"]["houses"][comp_key]["remaining_months"] = m_months
                            logic.save(data)
                            st.rerun()
                        else:
                            st.error("Not enough money for downpayment")

                st.divider()

                if owned_count > 0:
                    if st.button(f"Sell 1 Unit", key=f"sell_{comp_key}", use_container_width=True):
                        data["money"] += last_entry
                        data["assets"]["houses"][comp_key]["owned"] -= 1
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

elif st.session_state.page == "budget":
    st.title("Monthly Budget")
    data = logic.read_save()

    salary_income = float(data.get("net income", 0))

    total_mortgage_cost = 0.0
    for house_name in data["assets"]["houses"]:
        house_info = data["assets"]["houses"][house_name]
        if house_info.get("mortgage_active"):
            total_mortgage_cost += float(house_info.get("monthly_payment", 0))

    if "user_custom_items" not in st.session_state:
        st.session_state.user_custom_items = []

    with st.expander("Add New Item"):
        description_col, amount_col, category_col = st.columns([2, 1, 1])
        with description_col:
            new_item_name = st.text_input("Item Name")
        with amount_col:
            new_item_amount = st.number_input("Dollar Amount", min_value=0.0, step=10.0)
        with category_col:
            new_item_type = st.selectbox("Type", ["Expense", "Income"])

        if st.button("Add to List", use_container_width=True):
            if new_item_name:
                st.session_state.user_custom_items.append({
                    "description": new_item_name,
                    "amount": new_item_amount,
                    "category": new_item_type
                })
                st.rerun()

    st.divider()

    st.markdown("### **Monthly Income**")
    income_sum = salary_income

    income_left, income_right = st.columns([3, 1])
    income_left.write("Monthly Net Income")
    income_right.write(f"${salary_income:,.2f}")

    for item in st.session_state.user_custom_items:
        if item["category"] == "Income":
            left_column, right_column = st.columns([3, 1])
            left_column.write(item["description"])
            right_column.write(f"${item['amount']:,.2f}")
            income_sum += item["amount"]

    st.markdown(f"**Total Income: ${income_sum:,.2f}**")
    st.write("")

    st.markdown("### **Monthly Expenses**")
    expense_sum = total_mortgage_cost

    expense_left, expense_right = st.columns([3, 1])
    expense_left.write("Mortgage Payments")
    expense_right.write(f"${total_mortgage_cost:,.2f}")

    for item in st.session_state.user_custom_items:
        if item["category"] == "Expense":
            left_column, right_column = st.columns([3, 1])
            left_column.write(item["description"])
            right_column.write(f"${item['amount']:,.2f}")
            expense_sum += item["amount"]

    st.markdown(f"**Total Expenses: ${expense_sum:,.2f}**")

    st.divider()

    remaining_balance = income_sum - expense_sum

    label_column, value_column = st.columns([3, 1])
    with label_column:
        st.markdown("### **Total (Income minus Expenses)**")
    with value_column:
        st.markdown(f"### **${remaining_balance:,.2f}**")

    if st.button("Back"):
        st.session_state.page = "home"
        st.rerun()

    if st.button("Clear Custom Items"):
        st.session_state.user_custom_items = []
        st.rerun()
