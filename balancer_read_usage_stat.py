import pickle
import pprint

try:
    with open("data.pkl", "rb") as f:
        data = pickle.load(f)

    pprint.pprint(data["stats"]["usage_stat"])
except FileNotFoundError:
    print("File not found.")
except Exception as e:
    print(f"An error occurred: {e}")