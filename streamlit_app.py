import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on Oct 7th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
total_sales_all = df['Sales'].sum()
total_profit_all = df['Profit'].sum()
overall_avg_profit_margin = (total_profit_all / total_sales_all * 100) if total_sales_all > 0 else 0

st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

st.write("## Question 1")
categories = df['Category'].unique().tolist()
selected_category = st.selectbox(
    "Select Category", categories)

st.write("## Question 2")
subcategories = df[df['Category'] == selected_category]['Sub_Category'].unique().tolist()
selected_subcategories = st.multiselect("Select Sub-Categories:", subcategories)

st.write("## Question 3")
filtered_data = df[df['Sub_Category'].isin(selected_subcategories)]
sales_by_month = filtered_data.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()
st.line_chart(sales_by_month, y="Sales")

total_sales = filtered_data['Sales'].sum()
total_profit = filtered_data['Profit'].sum()
overall_profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
margin_difference = overall_profit_margin - overall_avg_profit_margin

st.write("## Question 4")
col1, col2, col3 = st.columns(3)
# Display metrics
col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Overall Profit Margin", f"{overall_profit_margin:.2f}%")

st.write("## Question 5")
col1, col2, col3 = st.columns(3)
# Display metrics
col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Overall Profit Margin", f"{overall_profit_margin:.2f}%", delta=f"{margin_difference:.2f}%")
