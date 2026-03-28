import pickle
import os

class Data():

    def __init__(self, name):
        self.name = name

    def write_pkl(self, input_data):
        with open("database.pkl", "wb") as f:
            pickle.dump(input_data, f)

    def read_pkl(self):
        if os.path.exists("database.pkl"):
            with open("database.pkl", "rb") as f:
                 return pickle.load(f)
        else:
            self.resetAll(self.name)
            return {}

    def update2(self, key1, key2, input_val):
        data = self.read_pkl()
        data[self.name][key1][key2] = input_val
        self.write_pkl(data)

    def update3(self, key1, key2, key3, input_val):
        data = self.read_pkl()
        data[self.name][key1][key2][key3] = input_val
        self.write_pkl(data)

    def get2(self, key1, key2):
        data = self.read_pkl()
        return data[self.name][key1][key2]

    def get3(self, key1, key2, key3):
        data = self.read_pkl()
        return data[self.name][key1][key2][key3]

    def resetAll(self, password):
        current_data = self.read_pkl()
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
        current_data[self.name] = starting_stats
        self.write_pkl(current_data)