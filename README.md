# E-Commerce Transaction Management and Anomaly Detection System

**Student:** IRAFASHA Schadrack (ID: 20251SEN246)  
**Course:** Database Development with PL/SQL (INSY 8311)  
**Instructor:** Eric Maniraguha  

## 1. Project Overview
This project designs and implements a database-driven system for e-commerce transactions. It normalizes raw e-commerce data into a 3NF Oracle schema and uses PL/SQL to detect suspicious, abnormal, or inconsistent records (anomalies) such as payment mismatches and late deliveries.

## 2. Data Source
Olist Brazilian E-Commerce Public Dataset (Kaggle). 
*   **Source:** https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
*   **Size:** 9 CSV files, ~100,000 orders (2016–2018).
*   **Licence:** CC BY-NC-SA 4.0.
*   **Details:** See `data/dataset_card.md` for quality checks and schema details.

## 3. Phase I – Business Process Modeling
*   **Process Modeled:** Order Fulfillment and Anomaly Flagging Process (To-Be design).
*   **Modeling Tool:** draw.io (diagrams.net).
*   **Published Diagram Link:** [INSERT YOUR PUBLIC DRAW.IO LINK HERE]
*   **Supporting Explanation:** [Link to `docs/business_process/business_process_explanation.pdf`]

## 4. Planned Database & PL/SQL Features
*   **Database:** 11 tables in 3NF (e.g., `orders`, `payments`, `order_items`, `anomaly_flags`, `audit_log`).
*   **PL/SQL Package:** `anomaly_pkg` containing detection functions, cursor-based batch jobs, and hold/release procedures.
*   **Triggers:** Enforce data integrity (e.g., blocking negative payments) and write to the `audit_log`.

## 5. Innovation
An interactive Streamlit analytics dashboard connected live to the Oracle PDB. It displays anomaly KPIs and allows analysts to resolve flags (e.g., release or cancel held orders) by calling PL/SQL procedures.

## 6. Repository Structure
*   `data/` - Raw CSVs and dataset card.
*   `docs/` - Phase deliverables (research, business process, normalization, data dictionary).
*   `scripts/` - Python scripts for data quality checking.
*   `innovation/` - Streamlit app code and documentation.
## 3. Phase I – Business Process Modeling
*   **Process Modeled:** Order Fulfillment and Anomaly Flagging Process
*   **Modeling Tool:** draw.io (diagrams.net)
*   **Published Diagram Link:** [https://viewer.diagrams.net/?tags=%7B%7D&lightbox=1&highlight=0000ff&edit=_blank&layers=1&nav=1&dark=auto#G12EL9N68xYNtwxG_dfGqb85h9q2TqcYqm](https://viewer.diagrams.net/?tags=%7B%7D&lightbox=1&highlight=0000ff&edit=_blank&layers=1&nav=1&dark=auto#G12EL9N68xYNtwxG_dfGqb85h9q2TqcYqm)
*   **Supporting Explanation:** [docs/business_process/business_process_explanation.pdf](docs/business_process/business_process_explanation.pdf)