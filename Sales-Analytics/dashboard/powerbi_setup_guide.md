# Power BI Dashboard Setup & Visual Rebuilding Guide

This guide walks you through loading the project dataset into Microsoft Power BI Desktop and reproducing the **Sales Performance & Business Intelligence Dashboard** shown in the executive screenshot.

---

## Step 1: Connect to the Dataset
1. Open **Power BI Desktop**.
2. Click **Get Data** > **Text/CSV**.
3. Browse to and select:
   `Sales-Analytics/dataset/sales_data.csv`
4. In the preview window, confirm encoding is **65001: Unicode (UTF-8)** and delimiter is **Comma**.
5. Click **Transform Data** to open Power Query Editor:
   - Ensure `Order_Date` and `Ship_Date` have data type `Date`.
   - Ensure `Sales`, `Cost`, `Profit`, `Unit_Price`, `Unit_Cost` have data type `Fixed Decimal Number` (`$` Currency).
   - Ensure `Quantity` has data type `Whole Number`.
   - Ensure `Discount` and `Profit_Margin` have data type `Percentage`.
6. Click **Close & Apply**.

---

## Step 2: Create the Date Table
In Power BI Desktop, go to **Modeling** tab > **New Table**, and enter:
```dax
DimDate = 
VAR MinDate = DATE(2024, 1, 1)
VAR MaxDate = DATE(2026, 12, 31)
RETURN
ADDCOLUMNS(
    CALENDAR(MinDate, MaxDate),
    "Year", YEAR([Date]),
    "Month Number", MONTH([Date]),
    "Month Name", FORMAT([Date], "mmm"),
    "Quarter", "Q" & FORMAT([Date], "q")
)
```
- Select column `Month Name` > Click **Sort by column** > Select `Month Number`.
- In Model View, create an active relationship:
  `DimDate[Date]` (1) -> `sales_orders[Order_Date]` (*)

---

## Step 3: Add Key DAX Measures
Create a dedicated measures table (**Enter Data** > Name it `_Measures`) and paste the formulas from `dashboard/dax_measures.dax`:
- `Total Sales = SUM(sales_orders[Sales])` (Format: `$#,##0` / `$0.0M`)
- `Profit Margin % = DIVIDE([Total Profit], [Total Sales], 0)` (Format: `0.0%`)
- `Total Units Sold = SUM(sales_orders[Quantity])` (Format: `#,##0` / `0.0K`)
- `Sales LY = CALCULATE([Total Sales], SAMEPERIODLASTYEAR('DimDate'[Date]))`
- `Sales YoY Growth % = DIVIDE([Total Sales] - [Sales LY], [Sales LY], 0)`
- `Profit Margin LY = CALCULATE([Profit Margin %], SAMEPERIODLASTYEAR('DimDate'[Date]))`
- `Profit Margin Delta Points = ([Profit Margin %] - [Profit Margin LY]) * 100`
- `Units Sold LY = CALCULATE([Total Units Sold], SAMEPERIODLASTYEAR('DimDate'[Date]))`
- `Units Sold YoY Growth % = DIVIDE([Total Units Sold] - [Units Sold LY], [Units Sold LY], 0)`

---

## Step 4: Build the Executive Summary Canvas Layout

### 1. Top KPI Cards (Top Banner)
- **Card 1 (Total Sales):**
  - Metric: `[Total Sales]` -> Displays `$24.8M`
  - Subtitle / Callout: `[Sales YoY Badge]` -> Displays `▲ +12.5% vs LY` (Green font `#27AE60`)
- **Card 2 (Profit Margin):**
  - Metric: `[Profit Margin %]` -> Displays `32.4%`
  - Subtitle: `[Profit Margin YoY Badge]` -> Displays `▲ +2.1% vs LY`
- **Card 3 (Units Sold):**
  - Metric: `[Total Units Sold]` -> Displays `18.6K`
  - Subtitle: `[Units Sold YoY Badge]` -> Displays `▲ +8.3% vs LY`
- **Card 4 (Revenue Growth Sparkline):**
  - Visual: Sparkline / Area Line chart showing monthly ups and downs.

### 2. Main Middle Visuals
- **Visual 1: Sales Trends (Revenue by Month & Forecast)**
  - Type: **Line and Clustered Column Chart** or **Line Chart**
  - X-Axis: `DimDate[Month Name]` (Jan - Dec)
  - Y-Axis: `[Total Sales]`
  - Forecast line: Add Analytics Pane > **Forecast** (Length: 2 months, Confidence: 95%) or add calculated measure `[Forecasted Revenue]`.
  - Format: Blue solid line (`#0066CC`) with circular markers.

- **Visual 2: Key Influencers (AI Visual)**
  - Visual: **Key Influencers** built-in visual
  - Analyze: `[Sales]`
  - Explain By: `Category`, `Region`, `Discount`, `Customer_Age_Group`
  - Settings: "What influences Revenue to Increase"
  - Key Findings generated:
    1. Product Category is Electronics (+23.5%)
    2. Region is West (+12.2%)
    3. Discount < 5% (+8.7%)
    4. Customer Age Group is 25-34 (+6.7%)

- **Visual 3: Sales by Region (US Map)**
  - Visual: **Shape Map** or **Azure Map** / Bubble Map
  - Location: `State`
  - Bubble Size / Color: `[Total Sales]`
  - Legend: `Region` (North, South, East, West)

- **Visual 4: Profit by Product Category**
  - Visual: **Clustered Bar Chart** (Horizontal)
  - Y-Axis: `sales_orders[Category]` (Electronics, Furniture, Clothing, Accessories)
  - X-Axis: `[Total Profit]` (showing $0M, $5M, $10M, $15M scale)
  - Data Labels: ON (Bold font `#333333`)
  - Bar color: Deep Blue (`#0066CC`)

- **Visual 5: AI Forecast (Next 6 Months)**
  - Visual: **Clustered Column Chart** with Trend Line
  - X-Axis: Month (Jan, Feb, Mar, Apr, May, Jun)
  - Y-Axis: Forecasted Sales
  - Trend line: ON (Black dashed line)

### 3. Bottom Page Tabs (Navigation Bar)
- Tab 1: **Executive Summary** (Active)
- Tab 2: **Sales Trends**
- Tab 3: **Customer Insights**
- Tab 4: **Product Analysis**
