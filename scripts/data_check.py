import pandas as pd
import os

# Set the path to your raw data folder
RAW_DIR = "D:\\E-Commerce-Transaction-Management-and-Anomaly-Detection-System\\data\\raw"

# Dictionary mapping table names to their exact CSV filenames
FILES = {
    "customers":    "olist_customers_dataset.csv",
    "sellers":      "olist_sellers_dataset.csv",
    "products":     "olist_products_dataset.csv",
    "orders":       "olist_orders_dataset.csv",
    "order_items":  "olist_order_items_dataset.csv",
    "payments":     "olist_order_payments_dataset.csv",
    "reviews":      "olist_order_reviews_dataset.csv",
    "geolocation":  "olist_geolocation_dataset.csv",
    "categories":   "product_category_name_translation.csv",
}

print("=====================================================")
print(" OLIST DATA QUALITY CHECK ")
print("=====================================================\n")

# 1. Check if files exist and count rows
print("--- 1. ROW COUNTS ---")
for name, f in FILES.items():
    path = os.path.join(RAW_DIR, f)
    if os.path.exists(path):
        df = pd.read_csv(path)
        print(f"{name:15s} : {len(df):>7} rows | {len(df.columns):>2} columns")
    else:
        print(f"{name:15s} : MISSING FILE (Expected at {path})")

print("\n--- 2. MISSING VALUES (Top issues only) ---")
for name, f in FILES.items():
    path = os.path.join(RAW_DIR, f)
    if not os.path.exists(path): continue
    df = pd.read_csv(path)
    miss = df.isna().sum()
    miss = miss[miss > 0]
    if len(miss) > 0:
        print(f"\n[{name}]")
        for col, n in miss.items():
            print(f"   {col:30s} : {n} missing")

print("\n--- 3. DUPLICATE FULL ROWS ---")
for name, f in FILES.items():
    path = os.path.join(RAW_DIR, f)
    if not os.path.exists(path): continue
    df = pd.read_csv(path)
    dupes = df.duplicated().sum()
    if dupes > 0:
        print(f"{name:15s} : {dupes} duplicate rows")

print("\n--- 4. THE 4 CRITICAL CHECKS (For Phase 1 & 2 Defense) ---")
try:
    payments = pd.read_csv(os.path.join(RAW_DIR, "olist_order_payments_dataset.csv"))
    items = pd.read_csv(os.path.join(RAW_DIR, "olist_order_items_dataset.csv"))
    orders = pd.read_csv(os.path.join(RAW_DIR, "olist_orders_dataset.csv"))
    
    # Check 1: Non-positive payments
    nonpos = (payments["payment_value"] <= 0).sum()
    print(f"Count 1 - Non-positive payments: {nonpos}")

    # Check 2: Payment mismatches
    paid = payments.groupby("order_id")["payment_value"].sum().rename("paid")
    expected = items.groupby("order_id").apply(
        lambda d: (d["price"] + d["freight_value"]).sum()
    ).rename("expected")
    
    merged = pd.concat([paid, expected], axis=1, join="inner")
    merged["diff"] = (merged["paid"] - merged["expected"]).abs()
    mismatch = merged[merged["diff"] > 0.01]
    
    print(f"Count 2 - Mismatched orders: {len(mismatch)}")

    # Check 3: Total orders
    total_orders = payments["order_id"].nunique()
    print(f"Count 3 - Total orders: {total_orders}")
    print(f"          Mismatch rate: {100*len(mismatch)/total_orders:.2f}%")

    # Check 4: Mismatches by type
    mismatch_ids = set(mismatch.index)
    mm = payments[payments["order_id"].isin(mismatch_ids)]
    by_type = mm.groupby("payment_type")["order_id"].nunique().sort_values(ascending=False)
    print("\nCount 4 - Mismatches by payment type:")
    for ptype, count in by_type.items():
        print(f"   {ptype:15s} : {count}")

except Exception as e:
    print(f"Error running critical checks: {e}")

print("\n--- 5. STATUS EXCLUSIONS (For ANOM_LATE_SHIPMENT) ---")
try:
    o = pd.read_csv(os.path.join(RAW_DIR, "olist_orders_dataset.csv"))
    status_counts = o["order_status"].value_counts()
    print("Order Statuses in Olist:")
    for status, count in status_counts.items():
        print(f"   {status:15s} : {count}")
except Exception as e:
    print(f"Error checking statuses: {e}")

print("\n--- 6. DELIVERY CHECKS ---")
try:
    o = pd.read_csv(os.path.join(RAW_DIR, "olist_orders_dataset.csv"))
    deliv = o[(o.order_status=="delivered") & (o.order_delivered_customer_date.isna())]
    print(f"Orders marked 'delivered' but missing delivery date: {len(deliv)}")

    o["order_delivered_customer_date"] = pd.to_datetime(o.order_delivered_customer_date, errors="coerce")
    o["order_estimated_delivery_date"] = pd.to_datetime(o.order_estimated_delivery_date, errors="coerce")
    late = (o.order_delivered_customer_date > o.order_estimated_delivery_date).sum()
    print(f"Orders delivered AFTER estimated date: {late}")
except Exception as e:
    print(f"Error checking delivery: {e}")

print("\n=====================================================")
print(" CHECK COMPLETE ")
print("=====================================================")