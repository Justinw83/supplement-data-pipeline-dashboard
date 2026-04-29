import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

##### Load the Data #####

# Read the CSV file
df = pd.read_csv("../data/raw/supplement_sales.csv")

# Preview the data
print("Raw Data Preview:")
print(df.head())

print("Column Information:")
print(df.info())

print("Numeric Columns' Statistics:")
print(df.describe())

##### Data Cleaning #####

# Convert the date column to Date datatype
df["Date"] = pd.to_datetime(df["Date"])

# Standarize columns names. (Lower case and replace space with underscores)
df.columns = df.columns.str.lower().str.replace(" ", "_")

# Check for missing values
print("Missing Values:")
print(df.isnull().sum()) # There are no missing values

# Validate Revenue is calculated correctly
# First calculate what revenue should be
df["calculated_revenue"] = df["units_sold"] * df["price"]

# If there is a meaningful difference, (>1) replace with the calculated value.
df["revenue"] = np.where(
    abs(df["revenue"] - df["calculated_revenue"]) > 1,
    df["calculated_revenue"],
    df["revenue"]
)

##### Create Features #####

# Return Rate
df["return_rate"] = np.where(
    df["units_sold"] > 0,
    df["units_returned"] / df["units_sold"],
    0
)

# Time Features
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["year_month"] = df["date"].dt.to_period("M").astype(str)

# Preview the data
print("Transformed data preview:")
print(df.head())

##### Create Dimension Tables #####

# dim_product
dim_products = df[["product_name", "category", "price"]].drop_duplicates().reset_index(drop=True)
dim_products["product_id"] = dim_products.index + 1

# dim_location
dim_location = df[["location"]].drop_duplicates().reset_index(drop=True)
dim_location["location_id"] = dim_location.index + 1

# dim_platform
dim_platform = df[["platform"]].drop_duplicates().reset_index(drop=True)
dim_platform["platform_id"] = dim_platform.index + 1

##### Map IDs back to main table #####

# Merge product_id
df = df.merge(dim_products, on=["product_name", "category", "price"], how="left")

# Merge location_id
df = df.merge(dim_location, on="location", how="left")

# Merge platform_id
df = df.merge(dim_platform, on="platform", how="left")

##### Create Fact table #####

fact_sales = df[[
    "date",
    "product_id",
    "location_id",
    "platform_id",
    "units_sold",
    "revenue",
    "units_returned",
    "return_rate",
    "discount",
    "year",
    "month",
    "year_month"
]]

##### Save to Database #####
print("Saving to database.")

engine = create_engine('sqlite:///supplement_sales.db')

dim_products.to_sql('dim_products', engine, if_exists='replace', index=False)
dim_location.to_sql('dim_location', engine, if_exists='replace', index=False)
dim_platform.to_sql('dim_platform', engine, if_exists='replace', index=False)
fact_sales.to_sql('fact_sales', engine, if_exists='replace', index=False)

print("\nData successfully loaded into SQLite database.")


##### Save CSV outputs #####

print("Saving tables as CSV files.")

dim_products.to_csv("../data/cleaned/dim_products.csv", index=False)
dim_location.to_csv("../data/cleaned/dim_location.csv", index=False)
dim_platform.to_csv("../data/cleaned/dim_platform.csv", index=False)
fact_sales.to_csv("../data/cleaned/fact_sales.csv", index=False)

print("CSV files saved successfully.")