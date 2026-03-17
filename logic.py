import pickle
import os

def write_pkl(input_data):
    with open("database.pkl", "wb") as f:
        pickle.dump(input_data, f)

def read_pkl():
    if os.path.exists("database.pkl"):
        try:
            with open("database.pkl", "rb") as f:
                return pickle.load(f)
        except (EOFError, pickle.UnpicklingError):
            return {}
    else:
        return {}

def update2(name, key1, key2, input_val):
    data = read_pkl()
    data[name][key1][key2] = input_val
    write_pkl(data)

def update3(name, key1, key2, key3, input_val):
    data = read_pkl()
    data[name][key1][key2][key3] = input_val
    write_pkl(data)

def get2(name, key1, key2):
    data = read_pkl()
    return data[name][key1][key2]

def get3(name, key1, key2, key3):
    data = read_pkl()
    return data[name][key1][key2][key3]

def resetAll(name, password):
    current_data = read_pkl()
    starting_stats = {
        "password": password,
        "month": 0,
        "bank": {
            "interest": {
                "type": "simple",
                "rate": 0.02
            },
            "money": 10000,
        },
        "assets": {
            "houses": {
                "owned": 0
            },
            "cars": {
                "owned": 0
            },
            "artwork": {
                "owned": 0
            }
        },
        "stocks": {
            "Dave and Son's Coal Mine": {"owned": 0, "price": 0, "price_history": []},
            "Xavier's Egg Farm": {"owned": 0, "price": 0, "price_history": []},
            "Mr. Fox's Chicken Company": {"owned": 0, "price": 0, "price_history": []},
            "Raymond's Water Company": {"owned": 0, "price": 0, "price_history": []}
        }
    }
    current_data[name] = starting_stats
    write_pkl(current_data)