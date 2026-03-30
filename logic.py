import json
import os
import numpy as np
import streamlit as st

starting_stats = {
    "money": 500000,
    "month": 0,
    "gross income": 0,
    "net income": 0,
    "jobs": {
        "farmer": {"gross income": 82000/12, "net income": 60500/12},
        "librarian": {"gross income": 78000/12, "net income": 58500/12},
        "plumber": {"gross income": 79500/12, "net income": 59500/12},
        "electrician": {"gross income": 80800/12, "net income": 60300/12},
        "pharmacist": {"gross income": 110500/12, "net income": 78600/12},
        "cashier": {"gross income": 36600/12, "net income": 30200/12},
        "construction worker": {"gross income": 62400/12, "net income": 48200/12}
    },
    "bank": {
        "interest": {"type": "simple", "rate": 0.02},
    },
    "assets": {
        "houses": {
            "single": {
                "owned": 0,
                "mortgage_active": False,
                "monthly_payment": 0,
                "remaining_months": 0,
                "history": [830951.0]
            },
            "townhouse": {
                "owned": 0,
                "mortgage_active": False,
                "monthly_payment": 0,
                "remaining_months": 0,
                "history": [407000.0]
            },
            "apartment": {
                "owned": 0,
                "mortgage_active": False,
                "monthly_payment": 0,
                "remaining_months": 0,
                "history": [375000.0]
            },
        },
        "cars": {"owned": 0},
        "artwork": {"owned": 0},
        "computers": {
            "microsoft laptop": {"owned": 0, "price": 1699, "history": [1699.0]},
            "macbook": {"owned": 0, "price": 1499, "history": [1499.0]},
            "chromebook": {"owned": 0, "price": 850, "history": [850.0]}
        }
    },
    "stocks": {
        "Dave and Son's Coal Mine": {"owned": 0, "price": 50, "price_history": [50.0]},
        "Xavier's Egg Farm": {"owned": 0, "price": 500, "price_history": [500.0]},
        "Mr. Fox's Chicken Company": {"owned": 0, "price": 93, "price_history": [93.0]},
        "Raymond's Water Company": {"owned": 0, "price": 1000, "price_history": [1000.0]}
    }
}

def save(data):
    with open("save.json", "w") as f:
        json.dump(data, f, indent=4)


def read_save():
    if os.path.exists("save.json"):
        with open("save.json", "r") as f:
            return json.load(f)

    else:
        return reset()


def reset():
    save(starting_stats)
    return starting_stats


def update_market():
    data = read_save()
    configs = {
        "Dave and Son's Coal Mine": {"drift": 0.03, "vol": 0.06},
        "Xavier's Egg Farm": {"drift": 0.008, "vol": 0.1},
        "Mr. Fox's Chicken Company": {"drift": 0.02, "vol": 0.12},
        "Raymond's Water Company": {"drift": 0.01, "vol": 0.08}
    }

    for name, stats in configs.items():
        current_price = data["stocks"][name]["price"]
        drift = stats["drift"]
        vol = stats["vol"]
        shock = np.random.normal(0, 1)

        change_factor = np.exp((drift - 0.5 * vol ** 2) + vol * shock)
        new_price = round(current_price * change_factor, 2)

        data["stocks"][name]["price"] = new_price
        data["stocks"][name]["price_history"].append(new_price)

    save(data)


def update_prices(current_price, drift, vol):
    dt = 1 / 12
    shock = np.random.normal(0, 1)

    exponent = (drift - 0.5 * vol ** 2) * dt + vol * np.sqrt(dt) * shock
    change_factor = np.exp(exponent)

    new_price = np.round(current_price * change_factor, 2)
    return new_price

def empty(num):
    for _ in range(num):
        st.write("\n")

def calculate_change(current_price, previous_price):
    difference = current_price - previous_price
    percentage_change = (difference / current_price) * 100
    return round(percentage_change, 2)


def update_simulation():
    data = read_save()
    data["money"] += data["net income"]

    for house_key in data["assets"]["houses"]:
        house = data["assets"]["houses"][house_key]
        if house.get("mortgage_active") and house.get("remaining_months", 0) > 0:
            data["money"] -= house["monthly_payment"]
            house["remaining_months"] -= 1
            if house["remaining_months"] <= 0:
                house["mortgage_active"] = False

    data["month"] += 1
    save(data)
    update_market()
    update_computer_value()
    update_house_prices()

def back_button():
    st.divider()
    if st.button("Back"):
        st.session_state.page = "home"
        st.rerun()
def back(page):
    st.divider()
    if st.button("Back"):
        st.session_state.page = page
        st.rerun()

def predict_value(purchase_price, months_passed, useful_life):
    depreciation_rate = 2 / useful_life
    years_passed = months_passed / 12
    base = max(0, 1 - depreciation_rate)
    market_value = purchase_price * (base ** years_passed)
    return round(max(market_value, 50), 2)
def update_computer_value():
    data = read_save()
    months = data["month"]
    initial_1 = data["assets"]["computers"]["microsoft laptop"]["history"][0]
    initial_2 = data["assets"]["computers"]["macbook"]["history"][0]
    initial_3 = data["assets"]["computers"]["chromebook"]["history"][0]

    data["assets"]["computers"]["microsoft laptop"]["history"].append(predict_value(initial_1, months, 7))
    data["assets"]["computers"]["macbook"]["history"].append(predict_value(initial_2, months, 6))
    data["assets"]["computers"]["chromebook"]["history"].append(predict_value(initial_3, months, 5))

    save(data)


def update_house_prices():
    data = read_save()
    current_1 = data["assets"]["houses"]["single"]["history"][-1]
    current_2 = data["assets"]["houses"]["townhouse"]["history"][-1]
    current_3 = data["assets"]["houses"]["apartment"]["history"][-1]

    data["assets"]["houses"]["single"]["history"].append(update_prices(current_1, 0.045, 0.12))
    data["assets"]["houses"]["townhouse"]["history"].append(update_prices(current_2, 0.035, 0.1))
    data["assets"]["houses"]["apartment"]["history"].append(update_prices(current_3, 0.03, 0.15))

    save(data)

def calculate_average_monthly_change(history):
    if len(history) < 2:
        return 0.0

    total_percentage_change = 0
    intervals = len(history) - 1

    for i in range(1, len(history)):
        previous_price = history[i - 1]
        current_price = history[i]

        if previous_price != 0:
            change = ((current_price - previous_price) / previous_price) * 100
            total_percentage_change += change

    return round(total_percentage_change / intervals, 2)



def calculate_simple_interest(principal, monthly_rate, months):
    return principal * (monthly_rate / 100) * months

def calculate_compound_interest(principal, monthly_rate, months):
    return principal * ((1 + (monthly_rate / 100)) ** months - 1)


def get_monthly_installment(principal, monthly_rate, months, interest_type):
    if interest_type == "simple":
        interest = calculate_simple_interest(principal, monthly_rate, months)
    else:
        interest = calculate_compound_interest(principal, monthly_rate, months)

    total_to_pay = principal + interest
    return round(total_to_pay / months, 2)
