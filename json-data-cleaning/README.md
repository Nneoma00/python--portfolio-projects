# JSON Data Cleaning Project

This project demonstrates how to clean messy JSON data and export the results into a new JSON file, based on a predefined schema.
It applies 2 methods for cleaning the input data:
* With JSON alone
* With Pandas

You can apply any of these, depending on your preference. However, the data cleaning process with JSON alone, took *0.01* seconds to complete. With Pandas however, 
the process took *0.10* seconds, likely due to the deduplication function I called in the script. 

Overall, using the Pandas module to clean JSON data is preferred for large and complex data sets.
This project only generates and cleans 200 customers' data.

## Project Overview
* Generates a JSON file with fake customer data (`generate_customers.py`)
* Loads the raw JSON file in each instance
* Cleans and transforms the data to fit the desired structure
* Saves the cleaned output

## How to Run
#[![Run on Replit](https://replit.com/badge/github/Nneoma00/your-repo)](https://replit.com/github/yourusername/your-repo)#
