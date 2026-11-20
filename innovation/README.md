# Innovation Layer: Streamlit Analytics Dashboard

## What it does
This layer provides an interactive web interface connected live to the Oracle PDB via Python (`oracledb`). 

## Features
*   **Anomaly Dashboard:** Displays KPIs (total anomalies, severity, resolution status) and a seller risk leaderboard.
*   **Actionable Controls:** A "Run Detection" button that executes `anomaly_pkg.run_all_detections`, and buttons to resolve flags (Release Order / Cancel Order) which execute PL/SQL procedures.

## Status
*(To be developed in Phase VII)*