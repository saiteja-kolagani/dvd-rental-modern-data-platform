DVD RENTAL — DIRTY RAW DATASET FOR ETL PRACTICE
====================================================

Purpose
-------
This dataset is intentionally dirty. It is designed for a real-world style
ETL/ELT project where raw source files are ingested first, then profiled,
validated, standardized, deduplicated, transformed and loaded into curated
analysis tables.

Tables included
---------------
- country: country_id, country, last_update
- city: city_id, city, country_id, last_update
- address: address_id, address, address2, district, city_id, postal_code, phone, last_update
- language: language_id, name, last_update
- category: category_id, name, last_update
- actor: actor_id, first_name, last_name, last_update
- film: film_id, title, description, release_year, language_id, rental_duration, rental_rate, length, replacement_cost, rating, special_features, fulltext, last_update
- film_actor: actor_id, film_id, last_update
- film_category: film_id, category_id, last_update
- inventory: inventory_id, film_id, store_id, last_update
- store: store_id, manager_staff_id, address_id, last_update
- staff: staff_id, first_name, last_name, address_id, email, store_id, active, username, password, last_update, picture
- customer: customer_id, store_id, first_name, last_name, email, address_id, activebool, create_date, last_update, active
- rental: rental_id, rental_date, inventory_id, customer_id, return_date, staff_id, last_update
- payment: payment_id, customer_id, staff_id, rental_id, amount, payment_date

Expected raw-data problems
--------------------------
1. Exact duplicate rows.
2. Business-key duplicates with different non-key attributes.
3. NULL/blank values.
4. Placeholder nulls: NULL, null, N/A, NA.
5. Leading/trailing whitespace.
6. Mixed text casing.
7. Mixed date/time formats.
8. Invalid dates such as 31/02/2026 and 2026-13-40.
9. Missing/invalid foreign keys.
10. Negative or malformed numeric values.
11. Numeric strings containing commas/spaces.
12. Invalid/unknown categorical values.
13. Mixed boolean representations: Y/N, yes/no, TRUE/FALSE, 1/0, active/inactive.
14. Malformed email addresses.
15. Inconsistent phone formats.
16. Missing primary/business keys in deliberately added edge records.
17. Referential-integrity violations across files.
18. Impossible business values, e.g. negative rental duration, negative payment,
    unrealistic release year.
19. Out-of-order and duplicate transaction records.
20. Some records intentionally contain multiple quality issues.

Suggested ETL layers
--------------------
RAW
  -> LANDING/BRONZE: preserve source exactly
  -> VALIDATED/SILVER: type conversion, null normalization, validation flags,
     rejected-record quarantine, referential checks
  -> CURATED/GOLD: deduplicated relational model / dimensional model
  -> ANALYTICS: revenue, rentals, customers, films, stores, staff metrics

Suggested validation rules
--------------------------
Primary keys:
  country.country_id
  city.city_id
  address.address_id
  language.language_id
  category.category_id
  actor.actor_id
  film.film_id
  inventory.inventory_id
  store.store_id
  staff.staff_id
  customer.customer_id
  rental.rental_id
  payment.payment_id

Composite keys:
  film_actor(actor_id, film_id)
  film_category(film_id, category_id)

Important foreign keys:
  city.country_id -> country.country_id
  address.city_id -> city.city_id
  film.language_id -> language.language_id
  film_actor.actor_id -> actor.actor_id
  film_actor.film_id -> film.film_id
  film_category.film_id -> film.film_id
  film_category.category_id -> category.category_id
  inventory.film_id -> film.film_id
  inventory.store_id -> store.store_id
  store.manager_staff_id -> staff.staff_id
  store.address_id -> address.address_id
  staff.address_id -> address.address_id
  staff.store_id -> store.store_id
  customer.store_id -> store.store_id
  customer.address_id -> address.address_id
  rental.inventory_id -> inventory.inventory_id
  rental.customer_id -> customer.customer_id
  rental.staff_id -> staff.staff_id
  payment.customer_id -> customer.customer_id
  payment.staff_id -> staff.staff_id
  payment.rental_id -> rental.rental_id

Recommended transformations
----------------------------
- Normalize null markers to actual NULL.
- Trim whitespace.
- Standardize casing for names/categorical values.
- Parse all dates into TIMESTAMP.
- Cast IDs to INTEGER.
- Cast monetary fields to NUMERIC(10,2).
- Standardize boolean values to TRUE/FALSE.
- Validate email and phone formats.
- Validate numeric ranges.
- Validate release_year.
- Validate return_date >= rental_date.
- Validate amount >= 0.
- Validate all foreign keys.
- Deduplicate exact duplicates.
- Apply a survivorship rule for business-key duplicates.
- Quarantine records that fail mandatory-field or referential checks.
- Preserve rejected rows with rejection_reason and source_file.

Important
---------
The dataset is synthetic and intentionally contains contradictions.
Do NOT expect every raw record to satisfy the relational model. That is
intentional and is part of the ETL challenge.

Recommended project challenge
-----------------------------
Build:
1. Python ingestion layer
2. Raw S3/local landing zone
3. Data-quality profiling
4. Validation framework
5. Invalid-record quarantine
6. Deduplication
7. PostgreSQL/Snowflake curated layer
8. Star-schema analytics layer
9. SQL data-quality checks
10. ETL logging and audit table
