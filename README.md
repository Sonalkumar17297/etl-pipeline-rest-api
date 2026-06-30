# ETL Pipeline: REST API → Pandas → SQLite → SQL Analysis

A complete end-to-end data pipeline that extracts data from a live REST API, transforms it using Pandas, loads it into a SQLite database, and analyzes it using SQL — demonstrating the full Extract, Transform, Load, Analyze (ETLA) workflow used in real-world data engineering.

## Overview

This project simulates a common data engineering task: pulling related data from two different sources, combining them, and producing analysis-ready insights. It pulls **users** and **posts** data from a public REST API, where each post is linked to a user (similar to how orders link to customers, or transactions link to accounts in real business systems).

## Pipeline Architecture

```
[REST API: /users]  ──┐
                       ├──→ [Pandas: Clean + Flatten + Merge] ──→ [SQLite DB] ──→ [SQL Analysis]
[REST API: /posts]  ──┘
```

## What This Project Demonstrates

- **Extract:** Pulling structured data from a live REST API using Python's `requests` library
- **Transform:** Flattening nested JSON structures (e.g., extracting `city` and `zipcode` from a nested `address` object), merging two related datasets on a foreign-key relationship, and resolving column-naming conflicts after a merge
- **Load:** Persisting cleaned, structured data into a SQLite database table
- **Analyze:** Writing SQL queries (`GROUP BY`, `COUNT`, `ORDER BY`, `LIMIT`) directly against the loaded data to answer real questions

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core scripting language |
| `requests` | API calls |
| `pandas` | Data cleaning, flattening, merging |
| `sqlite3` | Lightweight database for the Load stage |
| SQL | Final analysis queries |

## Data Source

Data is sourced from [JSONPlaceholder](https://jsonplaceholder.typicode.com/), a free, public mock API commonly used for prototyping and testing. This is **practice/mock data**, not real business data — the project is intentionally built to demonstrate pipeline mechanics and technical execution, which transfer directly to real-world datasets (e.g., e-commerce orders, customer activity logs).

**Endpoints used:**
- `GET /users` — user profile data (includes nested `address` and `company` objects)
- `GET /posts` — posts authored by users, linked via `userId`

## Key Technical Challenges Solved

1. **Nested JSON flattening** — The API returns `address` and `company` as nested dictionaries within each user record. These were flattened into individual columns (`city`, `zipcode`, `company_name`) using `.apply()` with lambda functions.
2. **Merge column conflicts** — Merging `posts` and `users` on `userId`/`id` produced duplicate `id` columns (`id_x`, `id_y`). These were explicitly renamed to `post_id` and `user_id` to keep the final dataset unambiguous.
3. **Foreign key relationship** — Posts are linked to users via `posts.userId = users.id`, mirroring standard relational patterns found in production databases.

## Sample Analysis Queries

```sql
-- Which city's users have written the most posts?
SELECT city, COUNT(*) AS post_count
FROM user_posts
GROUP BY city
ORDER BY post_count DESC;

-- Which company has the most posts written by its employees?
SELECT company_name, COUNT(*) AS post_count
FROM user_posts
GROUP BY company_name
ORDER BY post_count DESC;

-- Who is the single most active user by post count?
SELECT name, COUNT(*) AS post_count
FROM user_posts
GROUP BY name
ORDER BY post_count DESC
LIMIT 1;
```

## How to Run This Project

```bash
pip install requests pandas

python etl_pipeline.py
```

This will:
1. Fetch user and post data from the API
2. Clean and merge the data
3. Load it into a local SQLite database (`project1.db`)
4. Print the results of the analysis queries to the console

## Project Structure

```
etl-pipeline-rest-api/
├── etl_pipeline.py      # Main pipeline script (Extract → Transform → Load → Analyze)
├── project1.db          # SQLite database (generated on run)
└── README.md
```

## Future Improvements

- Add error handling and retry logic for API calls
- Incorporate a third related dataset (e.g., `/comments`) for more complex joins
- Add basic logging to track pipeline execution
- Parameterize the pipeline to run on a schedule (e.g., via cron or Airflow)

## Author

Built as a hands-on practice project to demonstrate end-to-end data engineering skills: API integration, data transformation, database loading, and SQL-based analysis.
