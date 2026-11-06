# Power BI Data Model Architecture & Schema Design

## 1. Overview
The **Sales Performance & Business Intelligence Dashboard** is engineered following enterprise data warehousing best practices using a pure **Star Schema** architecture. This ensures optimal DAX performance, minimizes memory footprint, enables seamless filter propagation, and prevents circular relationship traps.

```
       +-----------------------+
       |       DimDate         |
       |-----------------------|
       | Date (PK)             |
       | Year, Month, Quarter  |
       | Month_Name, Day       |
       +-----------+-----------+
                   | 1
                   |
                   | *
       +-----------v-----------+
       |       FactSales       |
       |  (sales_orders table) |
       |-----------------------|
       | Order_ID              |
       | Customer_ID (FK)      |------+
       | Product_ID (FK)       |      |
       | Location_ID / State   |      |
       | Order_Date (FK)       |      |
       | Ship_Date             |      |
       | Sales, Profit, Cost   |      |
       | Quantity, Discount    |      |
       +-----------+-----------+      |
                   | *                |
                   |                  |
                   | 1                | *
       +-----------v-----------+      |   +-----------------------+
       |      DimProduct       |      +-->|      DimCustomer      |
       |-----------------------|          |-----------------------|
       | Product_ID (PK)       |          | Customer_ID (PK)      |
       | Product_Name          |          | Customer_Name         |
       | Category              |          | Customer_Segment      |
       | Sub_Category          |          | Customer_Age_Group    |
       | Unit_Price, Base_Cost |          | Customer_Gender       |
       +-----------------------+          +-----------------------+
```

---

## 2. Table Specifications & Cardinalities

### Fact Table: `FactSales` (Grain: 1 Line Item per Order)
- **Primary Key:** `Order_Line_ID` (or composite `Order_ID` + `Product_ID`)
- **Foreign Keys:**
  - `Order_Date` -> `DimDate[Date]` (Many-to-One, Single direction)
  - `Customer_ID` -> `DimCustomer[Customer_ID]` (Many-to-One, Single direction)
  - `Product_ID` -> `DimProduct[Product_ID]` (Many-to-One, Single direction)
  - `State` / `Region` -> `DimGeography[State]` (Many-to-One, Single direction)
- **Metrics / Additive Measures:** `Gross_Sales`, `Discount_Amount`, `Sales`, `Cost`, `Profit`, `Quantity`.

### Dimension Table: `DimDate`
Generated using Power BI DAX `CALENDARAUTO()` or Power Query:
```dax
DimDate = 
VAR MinYear = 2024
VAR MaxYear = 2026
RETURN
ADDCOLUMNS(
    CALENDAR(DATE(MinYear, 1, 1), DATE(MaxYear, 12, 31)),
    "Year", YEAR([Date]),
    "Month Number", MONTH([Date]),
    "Month Name", FORMAT([Date], "mmm"),
    "Month Year", FORMAT([Date], "mmm yyyy"),
    "Month Year Order", YEAR([Date]) * 100 + MONTH([Date]),
    "Quarter", "Q" & FORMAT([Date], "q"),
    "Year-Quarter", FORMAT([Date], "yyyy") & " Q" & FORMAT([Date], "q"),
    "Day of Week", FORMAT([Date], "dddd"),
    "IsWeekend", IF(WEEKDAY([Date], 2) >= 6, 1, 0)
)
```

### Dimension Table: `DimCustomer`
- **Fields:** `Customer_ID`, `Customer_Name`, `Customer_Segment` (Consumer, Corporate, Home Office), `Customer_Age_Group` (18-24, 25-34, 35-44, 45-54, 55+), `Customer_Gender`.

### Dimension Table: `DimProduct`
- **Fields:** `Product_ID`, `Product_Name`, `Category` (Electronics, Furniture, Clothing, Accessories), `Sub_Category`, `Unit_Cost`, `Unit_Price`.

### Dimension Table: `DimGeography`
- **Fields:** `City`, `State`, `Region` (West, East, South, North), `Postal_Code`, `Country`.

---

## 3. Modeling Best Practices Applied
1. **One-Way Filter Flow (Single Direction):** All relationships flow from 1 (Dimension) to Many (Fact table) to prevent ambiguous filter contexts and performance bottlenecks.
2. **Hidden Foreign Keys:** Foreign keys in `FactSales` are hidden in Report view to enforce the use of dimension attributes for slicing and grouping.
3. **Explicit Measures:** All numeric aggregations are authored as explicit DAX measures (`[Total Sales]`, `[Profit Margin %]`), never implicit default sums.
4. **Sort By Column:** `Month Name` is sorted by `Month Number` or `Month Year Order` to ensure correct chronological sorting on line charts.
