# Supplement Sales Data Pipeline & Dashboard

## Overview
This project demonstrates an end-to-end data pipeline and analytics dashboard built using supplement sales data.

## Data Source

Dataset: "Supplement Sales Data"  
Source: Kaggle  
Link: https://www.kaggle.com/datasets/zahidmughal2343/supplement-sales-data/data

This dataset includes weekly sales data across multiple supplement categories, platforms, and geographic locations.

## Data Pipeline
- Cleaned and transformed raw data using Python
- Created fact and dimension tables
- Loaded data into a SQLite database
- Created csv files for the fact and dimension tables for the purpose of this project

## Data Model

A star schema was implemented to organize the data for analysis.

**Fact Table:**
- fact_sales: Contains transactional data including revenue, units sold, and return rate

**Dimension Tables:**
- dim_products: Product-level details (name, category, price)
- dim_location: Geographic information (country)
- dim_platform: Sales channel information (Amazon, Walmart, iHerb)

This structure allows for efficient querying and flexible analysis across multiple business dimensions.

## Dashboard
The Tableau dashboard includes:
- KPI metrics (Revenue, Units Sold, Return Rate)
- Revenue breakdown by category and platform
- Interactive filtering
- Live Dashboard: https://public.tableau.com/views/SupplementSalesDashboard_17774211180250/ExecutiveOverview?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link

## Data Notes

Data from 2025 represents a partial year and was excluded from dashboard visualizations to avoid misleading comparisons with full-year data.

## Key Insights
- Revenue is evenly distributed across platfoms
- Four categories (vitamins, minerals, performance, protein) carry the bulk of the revenue
- Return rates remain low across products and platforms

## Tools Used
- Python (pandas, numpy)
- SQLite
- Tableau Public
