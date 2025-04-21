import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def main():
    file = st.file_uploader("Pick a file")
    if file is not None:
        df = pd.read_csv(file)
        st.subheader("Data Preview")
        st.dataframe(df.head())
        
        # Sales Summary
        st.subheader("Sales Summary")

        total_sales = df['revenue'].sum()
        total_units = df['units_sold'].sum()

        avg_revenue = df['revenue'].mean()

        st.write(f"Total Sales: s{total_sales:.2f}")
        st.write(f"Total Units Sold: {total_units}")
        st.write(f"Average Revenue per Sale: ${avg_revenue:,.2f}")

        # Sales by Region
        st.subheader("Sales by Region")

        sales_by_region = df.groupby('region').agg({'revenue':'sum', 'units_sold':'sum'}).reset_index()
        fig, ax = plt.subplots()
        sales_by_region.plot(kind='bar', x='region', y='revenue', ax=ax, color='red', legend=False)
        ax.set_title("Revenue by Region")
        ax.set_ylabel("Revenue")
        st.pyplot(fig)

        # Sales by Sales Rep
        st.subheader("Sales by Sales Rep")

        sales_by_rep = df.groupby('sales_rep').agg({'revenue': 'sum', 'units_sold': 'sum'}).reset_index()

        fig, ax = plt.subplots()
        sales_by_rep.plot(kind='bar', x='sales_rep', y='revenue', ax=ax, color='green', legend=False)
        ax.set_title("Revenue by Sales Rep")
        ax.set_ylabel("Revenue")
        st.pyplot(fig)

        # Customer Insights
        st.subheader("Customer Insights")

        avg_age = df['customer_age'].mean()

        st.write(f"Average Customer Age: {avg_age:.2f}")

        fig, ax = plt.subplots()
        df['customer_age'].hist(bins=5, ax=ax, color="purple", alpha=0.6)
        ax.set_title("Customer Rating Distribution")
        ax.set_xlabel("Rating")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)

        new_customers_sales = df[df['is_new_customer'] == True].agg({'revenue': 'sum', 'units_sold': 'sum'})
        existing_customers_sales = df[df['is_new_customer'] == True].agg({'revenue': 'sum', 'units_sold': 'sum'})

        st.write("Sales for New Customers:")
        st.write(new_customers_sales)

        st.write("Sales for Returning Customers:")
        st.write(existing_customers_sales)
        
        # Sales Over Time
        st.subheader("Sales Over Time")

        df['date'] = pd.to_datetime(df['date'])
        sales_by_date = df.groupby('date').agg({'revenue': 'sum', 'units_sold': 'sum'}).reset_index()

        # Line plot for sales over time
        fig, ax = plt.subplots()
        sales_by_date.plot(x='date', y='revenue', ax=ax, color='orange', legend=False)
        ax.set_title("Sales Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Revenue")
        st.pyplot(fig)



if __name__ == "__main__":
    main()
