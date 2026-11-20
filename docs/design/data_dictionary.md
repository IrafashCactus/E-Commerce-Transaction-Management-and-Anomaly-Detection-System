# Data Dictionary  Logical Design

## 1. `product_categories`
| Column | Type | Required | Unique | Meaning |
| :--- | :--- | :--- | :--- | :--- |
| category_id | VARCHAR | Yes (PK) | Yes | Portuguese category name |
| category_name_en | VARCHAR | Yes | No | English translation |

## 2. `geolocation`
| Column | Type | Required | Unique | Meaning |
| :--- | :--- | :--- | :--- | :--- |
| zip_prefix | VARCHAR | Yes (PK) | Yes | First 5 digits of zip code |
| lat | NUMBER | Yes | No | Latitude |
| lng | NUMBER | Yes | No | Longitude |
| city | VARCHAR | Yes | No | City name |
| state | VARCHAR | Yes | No | 2-letter state code |

## 3. `customers`
| Column | Type | Required | Unique | Meaning |
| :--- | :--- | :--- | :--- | :--- |
| customer_id | VARCHAR | Yes (PK) | Yes | Unique per order |
| customer_unique_id | VARCHAR | Yes | No | Unique per person |
| zip_prefix | VARCHAR | Yes (FK) | No | Links to geolocation |
| city | VARCHAR | Yes | No | City name |
| state | VARCHAR | Yes | No | State code |

## 4. `sellers`
| Column | Type | Required | Unique | Meaning |
| :--- | :--- | :--- | :--- | :--- |
| seller_id | VARCHAR | Yes (PK) | Yes | Unique seller ID |
| zip_prefix | VARCHAR | Yes (FK) | No | Links to geolocation |
| city | VARCHAR | Yes | No | City name |
| state | VARCHAR | Yes | No | State code |

## 5. `products`
| Column | Type | Required | Unique | Meaning |
| :--- | :--- | :--- | :--- | :--- |
| product_id | VARCHAR | Yes (PK) | Yes | Unique product ID |
| category_id | VARCHAR | No (FK) | No | Links to product_categories |
| name_length | NUMBER | No | No | Length of product name |
| description_length | NUMBER | No | No | Length of description |
| photos_qty | NUMBER | No | No | Number of photos |
| weight_g | NUMBER | No | No | Weight in grams |
| length_cm | NUMBER | No | No | Length in cm |
| height_cm | NUMBER | No | No | Height in cm |
| width_cm | NUMBER | No | No | Width in cm |

## 6. `orders`
| Column | Type | Required | Unique | Meaning |
| :--- | :--- | :--- | :--- | :--- |
| order_id | VARCHAR | Yes (PK) | Yes | Unique order ID |
| customer_id | VARCHAR | Yes (FK) | No | Links to customers |
| order_status | VARCHAR | Yes | No | Current status |
| purchase_ts | TIMESTAMP | Yes | No | When order was placed |
| approved_at | TIMESTAMP | No | No | When payment approved |
| delivered_carrier_date | TIMESTAMP | No | No | Handoff to carrier |
| delivered_customer_date | TIMESTAMP | No | No | Delivered to customer |
| estimated_delivery_date | TIMESTAMP | Yes | No | Promised delivery date |

## 7. `order_items`
| Column | Type | Required | Unique | Meaning |
| :--- | :--- | :--- | :--- | :--- |
| order_id | VARCHAR | Yes (PK) | No | Links to orders |
| order_item_id | NUMBER | Yes (PK) | No | Line number (1, 2, 3...) |
| product_id | VARCHAR | Yes (FK) | No | Links to products |
| seller_id | VARCHAR | Yes (FK) | No | Links to sellers |
| shipping_limit_date | TIMESTAMP | Yes | No | Seller's deadline to ship |
| price | NUMBER | Yes | No | Item price (BRL) |
| freight_value | NUMBER | Yes | No | Shipping cost (BRL) |

## 8. `payments`
| Column | Type | Required | Unique | Meaning |
| :--- | :--- | :--- | :--- | :--- |
| order_id | VARCHAR | Yes (PK) | No | Links to orders |
| payment_sequential | NUMBER | Yes (PK) | No | Sequence (1, 2...) |
| payment_type | VARCHAR | Yes | No | credit_card, boleto, voucher, debit_card, refund (design extension) |
| payment_installments | NUMBER | Yes | No | Number of installments |
| payment_value | NUMBER | Yes | No | Payment amount (BRL) |

## 9. `reviews`
| Column | Type | Required | Unique | Meaning |
| :--- | :--- | :--- | :--- | :--- |
| review_id | VARCHAR | Yes (PK) | Yes | Unique review ID |
| order_id | VARCHAR | Yes (FK) | No | Links to orders |
| review_score | NUMBER | Yes | No | 1 to 5 stars |
| comment_title | VARCHAR | No | No | Short title |
| comment_message | VARCHAR | No | No | Full review text |
| creation_date | DATE | Yes | No | Date review created |
| answer_timestamp | TIMESTAMP | No | No | When seller responded |

## 10. `anomaly_flags` (Design Extension)
| Column | Type | Required | Unique | Meaning |
| :--- | :--- | :--- | :--- | :--- |
| flag_id | NUMBER | Yes (PK) | Yes | Auto-increment ID |
| order_id | VARCHAR | No (FK) | No | Links to orders (NULL for seller-level flags) |
| seller_id | VARCHAR | No (FK) | No | Links to sellers (only for seller-level flags) |
| rule_code | VARCHAR | Yes | No | e.g., ANOM_PAY_MISMATCH |
| severity | VARCHAR | Yes | No | LOW, MEDIUM, HIGH |
| status | VARCHAR | Yes | No | new, resolved, closed |
| detected_at | TIMESTAMP | Yes | No | When flag was raised |
| resolved_at | TIMESTAMP | No | No | When flag was closed |
| previous_order_status | VARCHAR | No | No | Status before on_hold |
| details | VARCHAR | No | No | Human-readable explanation |

## 11. `audit_log` (Design Extension)
| Column | Type | Required | Unique | Meaning |
| :--- | :--- | :--- | :--- | :--- |
| audit_id | NUMBER | Yes (PK) | Yes | Auto-increment ID |
| table_name | VARCHAR | Yes | No | Table that was changed |
| action | VARCHAR | Yes | No | INSERT, UPDATE, DELETE |
| ref_id | VARCHAR | No | No | Primary key of affected row |
| user_id | VARCHAR | No | No | Database user |
| details | VARCHAR | No | No | Description of change |
| action_ts | TIMESTAMP | Yes | No | When action occurred |