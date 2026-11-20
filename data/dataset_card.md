## 3. Data Quality Check (Counts observed, NOT fixed)
*These counts were computed using a Python script (see `scripts/data_check.py`). No data has been cleaned yet.*

### 3.1 Row Counts
| Table | Rows | Columns |
| :--- | :--- | :--- |
| customers | 99,441 | 5 |
| sellers | 3,095 | 4 |
| products | 32,951 | 9 |
| orders | 99,441 | 8 |
| order_items | 112,650 | 7 |
| payments | 103,886 | 5 |
| reviews | 99,224 | 7 |
| geolocation | 1,000,163 | 5 |
| categories | 71 | 2 |

### 3.2 Missing Values
*   **products:** 610 missing `product_category_name`, 610 missing name/description lengths, 2 missing dimensions.
*   **orders:** 160 missing `order_approved_at`, 1,783 missing `order_delivered_carrier_date`, 2,965 missing `order_delivered_customer_date`.
*   **reviews:** 87,656 missing `review_comment_title`, 58,247 missing `review_comment_message`.

### 3.3 Duplicates
*   **geolocation:** 261,831 duplicate rows (multiple points per zip code).

### 3.4 Critical Anomaly Counts (For Phase 1/2 Defense)
*   **Non-positive payments:** 9 orders (payment_value ≤ 0).
*   **Payment mismatches:** 380 orders (0.38% of 99,440 total orders). 
    *   Breakdown: Credit Card (340), Boleto (29), Voucher (11), Debit Card (10).
*   **Late deliveries:** 7,827 orders delivered after the estimated date.
*   **Missing delivery dates:** 8 orders marked 'delivered' with no delivery timestamp.

### 3.5 Order Statuses (For Exclusions)
*   delivered (96,478), shipped (1,107), canceled (625), unavailable (609), invoiced (314), processing (301), created (5), approved (2).