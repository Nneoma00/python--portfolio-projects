import json
import pandas as pd
import time

start_time = time.time()
with open('old_customers.json', 'r') as f:
    crm_data = json.load(f)

client_deets = crm_data.get("customers", [])

#Load into a dataframe
df = pd.DataFrame(client_deets)

#Remove duplicates
df.drop_duplicates() #we go from there

#drop unwanted columns:
#df_cleaned = df_cleaned.drop(columns=["age"], errors="ignore")
#or keep wanted columns or response fields
keep_columns = ["name", "email", "phone", "membership_level"]
#Select only those columns i Wanna keep
df_cleaned = df[keep_columns]


def transform_fields(row):
    return {
        "full_name": row.get("name", "Unknown"),
        "email_address": row.get("email", "N/A"),
        "mobile": row.get("phone", "N/A"),
        "tier": row.get("membership_level", "N/A"),
    }

#Apply schema transformation
transformed_data = [transform_fields(row) for row in df_cleaned.to_dict(orient="records")]

#Save the cleaned data
output_data = {"customers": transformed_data}
output_file = "cleaned_customer_data.json"
with open(output_file, "w") as f:
    json.dump(output_data, f, indent=4)

end_time = time.time()
elapsed_time = end_time - start_time

print(f"Transformed data saved to {output_file}")
print(f"Processing data took {elapsed_time:.2f} seconds")
