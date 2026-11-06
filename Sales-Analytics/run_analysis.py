"""
Sales-Analytics Runner Script
Executes all SQL queries and Python analyses directly against sales_analytics.db and sales_data.csv.
"""
import os
import sqlite3
import pandas as pd

base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "sql", "sales_analytics.db")
csv_path = os.path.join(base_dir, "dataset", "sales_data.csv")

print("=" * 70)
print("  SALES PERFORMANCE & BUSINESS INTELLIGENCE DASHBOARD")
print("=" * 70)

# Check database
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    print("\n[+] Connected to SQLite Database: sql/sales_analytics.db")
    
    # 1. Executive KPIs
    kpi_sql = """
    SELECT 
        Year,
        ROUND(SUM(Sales), 2) AS Total_Sales,
        ROUND(SUM(Profit), 2) AS Total_Profit,
        ROUND(SUM(Profit) * 100.0 / SUM(Sales), 2) AS Profit_Margin_Pct,
        SUM(Quantity) AS Total_Units_Sold,
        COUNT(DISTINCT Order_ID) AS Total_Orders
    FROM sales_orders
    GROUP BY Year
    ORDER BY Year;
    """
    df_kpi = pd.read_sql_query(kpi_sql, conn)
    print("\n--- 1. Executive Scoreboard (FY 2024 vs FY 2025) ---")
    print(df_kpi.to_string(index=False))
    
    # 2. Regional Breakdown
    reg_sql = """
    SELECT 
        Region,
        ROUND(SUM(Sales), 2) AS Total_Revenue,
        ROUND(SUM(Profit), 2) AS Total_Profit,
        ROUND(SUM(Profit) * 100.0 / SUM(Sales), 2) AS Margin_Pct,
        COUNT(DISTINCT Customer_ID) AS Total_Customers,
        DENSE_RANK() OVER (ORDER BY SUM(Sales) DESC) AS Revenue_Rank
    FROM sales_orders
    WHERE Year = 2025
    GROUP BY Region
    ORDER BY Total_Revenue DESC;
    """
    df_reg = pd.read_sql_query(reg_sql, conn)
    print("\n--- 2. Regional Performance Matrix (2025) ---")
    print(df_reg.to_string(index=False))
    
    # 3. Category Breakdown
    cat_sql = """
    SELECT 
        Category,
        ROUND(SUM(Sales), 2) AS Revenue,
        ROUND(SUM(Profit), 2) AS Net_Profit,
        ROUND(SUM(Profit) * 100.0 / SUM(Sales), 2) AS Margin_Pct,
        ROUND(SUM(Sales) * 100.0 / (SELECT SUM(Sales) FROM sales_orders WHERE Year = 2025), 2) AS Pct_Share
    FROM sales_orders
    WHERE Year = 2025
    GROUP BY Category
    ORDER BY Revenue DESC;
    """
    df_cat = pd.read_sql_query(cat_sql, conn)
    print("\n--- 3. Category Breakdown (2025) ---")
    print(df_cat.to_string(index=False))
    
    # 4. Key Influencer Check: Discount Elasticity
    disc_sql = """
    SELECT 
        CASE 
            WHEN Discount = 0.0 THEN '0% (Full Price)'
            WHEN Discount <= 0.05 THEN '< 5% (Minimal)'
            WHEN Discount <= 0.10 THEN '5% - 10% (Moderate)'
            WHEN Discount <= 0.15 THEN '11% - 15% (High)'
            ELSE '> 15% (Steep)'
        END AS Discount_Tier,
        COUNT(*) AS Orders,
        ROUND(SUM(Sales), 2) AS Total_Sales,
        ROUND(SUM(Profit) * 100.0 / SUM(Sales), 2) AS Realized_Margin_Pct
    FROM sales_orders
    WHERE Year = 2025
    GROUP BY Discount_Tier
    ORDER BY Discount_Tier;
    """
    df_disc = pd.read_sql_query(disc_sql, conn)
    print("\n--- 4. Discount Impact & Margin Dilution (2025) ---")
    print(df_disc.to_string(index=False))
    
    conn.close()
else:
    print(f"[-] Database not found at: {db_path}")

print("\n" + "=" * 70)
print("  PROJECT FILES READY ON YOUR DESKTOP:")
print("  - Interactive Dashboard : dashboard/interactive_dashboard.html (Double-click to open!)")
print("  - Power BI File         : dashboard/sales_dashboard.pbix")
print("  - Jupyter Notebook      : notebooks/sales_analysis.ipynb")
print("  - SQL Analysis Queries  : sql/analysis_queries.sql")
print("=" * 70)
