from faker import Faker
import json

# Initialize Faker instance
fake = Faker()

# Generate random customer data
def generate_customers(num_customers=200):
    customers = []
    for i in range(1, num_customers + 1):
        customers.append({
            "customer_id": i,
            "name": fake.name(),
            "email": fake.email(),
            "phone": fake.phone_number(),
            "address": fake.address(),
            "membership_level": fake.random_element(["Basic", "Premium", "Gold"]),
        })
    return {"customers" : customers}

# Save to JSON file
def save_to_json(data, filename="old_customers.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

# Generate and save customer data
customers_data = generate_customers()
save_to_json(customers_data)
print("Customer data generated and saved to 'old_customers.json'")
