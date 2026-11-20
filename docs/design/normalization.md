# Normalization Walkthrough: UNF to 3NF

This document demonstrates the step-by-step normalization of the Olist e-commerce dataset from an Unnormalized Form (UNF) to Third Normal Form (3NF). 

## Step 1: Unnormalized Form (UNF)
**What it is:** One massive, wide table containing all data. It has repeating groups and mixed entities.
**Example of a raw UNF record (merging orders, items, payments, products, and customers):**

| order_id | customer_id | customer_city | order_status | product_id | product_category | price | freight | payment_type | payment_value | seller_id |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 0008288... | 9795a4... | sao paulo | delivered | 368c6c... | moveis | 49.90 | 13.37 | credit_card | 113.18 | 1f50f9... |
| 0008288... | 9795a4... | sao paulo | delivered | 368c6c... | moveis | 49.90 | 13.37 | credit_card | 113.18 | 1f50f9... |

*   **Problem:** The order `0008288...` has two identical items. The product, customer, and payment details are repeated. If the customer's city changes, we have to update every single row. 

---

## Step 2: First Normal Form (1NF)
**Goal:** Remove repeating groups. Every cell must hold a single value, and each row must be unique (usually by adding a composite primary key).

**Action taken:** We separate the line items. We create a composite key of `order_id` + `order_item_id`. 
*Dependency removed:* Repeating group of products inside a single order.

| order_id | order_item_id | customer_id | product_id | category | price | payment_type | payment_value | seller_id |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 0008288... | 1 | 9795a4... | 368c6c... | moveis | 49.90 | credit_card | 113.18 | 1f50f9... |
| 0008288... | 2 | 9795a4... | 368c6c... | moveis | 49.90 | credit_card | 113.18 | 1f50f9... |

*   **Problem:** The `customer_id`, `payment_type`, and `payment_value` depend *only* on the `order_id`, not on the specific `order_item_id`. This is a partial dependency.

---

## Step 3: Second Normal Form (2NF)
**Goal:** Remove partial dependencies. All non-key columns must depend on the *entire* primary key.

**Action taken:** We split the data into three tables: `orders` (customer/payment info), `order_items` (product/price info), and `payments` (split from orders because one order can have multiple payment methods like voucher + credit card).
*Dependency removed:* Partial dependency (customer, payment, and order status moved out of the items table).

**Table A: `orders`** (Depends only on `order_id`)
| order_id | customer_id | order_status |
| :--- | :--- | :--- |
| 0008288... | 9795a4... | delivered |

**Table B: `order_items`** (Depends on `order_id` + `order_item_id`)
| order_id | order_item_id | product_id | seller_id | price | freight_value |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 0008288... | 1 | 368c6c... | 1f50f9... | 49.90 | 13.37 |
| 0008288... | 2 | 368c6c... | 1f50f9... | 49.90 | 13.37 |

**Table C: `payments`** (Depends on `order_id` + `payment_sequential`)
| order_id | payment_seq | payment_type | payment_value |
| :--- | :--- | :--- | :--- |
| 0008288... | 1 | credit_card | 113.18 |

*   **Problem:** The `product_id` (368c6c...) determines the product category ("moveis") and dimensions. This is a transitive dependency: `order_id` → `product_id` → `category`.

---

## Step 4: Third Normal Form (3NF)
**Goal:** Remove transitive dependencies. Non-key columns must not depend on other non-key columns.

**Action taken:** We extract product details into a `products` table, and category names into a `product_categories` table. We also extract seller details into a `sellers` table.
*Dependency removed:* Transitive dependency (product category depends on product_id, not order_id).

**Table D: `products`**
| product_id | category_id | weight_g |
| :--- | :--- | :--- |
| 368c6c... | moveis | 225 |

**Table E: `product_categories`**
| category_id | category_name_en |
| :--- | :--- |
| moveis | furniture |

**Table F: `sellers`**
| seller_id | city | state |
| :--- | :--- | :--- |
| 1f50f9... | sao paulo | SP |

*(Note: The `order_items` table now contains only the Foreign Keys `product_id` and `seller_id`).*

---

## Summary of Tables Generated (11 Total)

The raw Olist CSV files were decomposed into the following 11 tables to achieve 3NF:

1.  **`product_categories`** (Category lookup)
2.  **`geolocation`** (Aggregated zip code lookup)
3.  **`customers`** (Customer geography)
4.  **`sellers`** (Seller geography)
5.  **`products`** (Product details)
6.  **`orders`** (Order status and timestamps)
7.  **`order_items`** (Line items linking orders to products and sellers)
8.  **`payments`** (Payment methods per order)
9.  **`reviews`** (Customer feedback)
10. **`anomaly_flags`** (Design extension for Phase 1 tracking)
11. **`audit_log`** (Design extension for Phase 6 tracking)

## Data Type Conversions (Cleaning Checklist for Phase IV)
*   `order_purchase_timestamp` and other timestamp columns are stored as TEXT in the CSV but will be converted to `TIMESTAMP` in Oracle.
*   `price` and `freight_value` are stored as FLOAT in the CSV but will be converted to `NUMBER(10,2)` in Oracle.