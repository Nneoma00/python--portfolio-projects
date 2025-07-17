#To check any customer contacts are missing
import json

with open("cleaned_customer_data.json") as file:
    data = json.load(file)

#for customer in data["customers"]:
print(len(data["customers"]))
