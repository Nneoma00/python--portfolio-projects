import json
import time

start_time = time.time()
with open('old_customers.json', 'r') as f:
    crm_data = json.load(f)
  
def transform_customers(record_or_data):
    return {
        "full_name": record_or_data["name"],
        "email_add" : record_or_data["email"],
        "phone_number": record_or_data["phone"],
        "tier": record_or_data["membership_level"],
    }
new_data = [transform_customers(customer) for customer in crm_data["customers"]]

output_file = "new_cs.json"
with open(output_file, "w") as f:
    json.dump(new_data, f, indent=4)

end_time = time.time()
elapsed_time = end_time - start_time

print(f"Transformed data saved to {output_file}")
print(f"Processing data took {elapsed_time:.2f} seconds")
