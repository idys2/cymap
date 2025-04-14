# Runs some comparison benchmarks between timescale and classic postgres
# to run: python -m backend.scripts.benchmark

import asyncio

from sqlalchemy.sql import text
from database.session import DatabaseSessionManager
from config import settings

QUERIES = {

    # two different versions of range-based aggregation:
    # 1. uses timescaledb's time_bucket function to group in a hypertable
    # 2. uses date_trunc to group in normal postgres
    "bucket": """
        SELECT time_bucket('1 minute', timestamp) AS bucket,
            AVG(value) AS avg_value
        FROM metrics
        GROUP BY bucket
        ORDER BY bucket ASC;
    """,
    "truncate": """
        SELECT date_trunc('minute', timestamp) AS bucket,
            AVG(value) AS avg_value
        FROM metrics
        GROUP BY bucket
        ORDER BY bucket ASC;
    """,

    # filtered aggregation 
    "filter": """
        SELECT type_id,
            AVG(value) AS avg_value, 
            MAX(value) AS min_value,
            MIN(value) AS max_value
        FROM metrics
        WHERE timestamp BETWEEN '2023-06-01 00:00:00+00' AND '2023-06-01 01:00:00+00'
        GROUP BY type_id;
    """,

    # point lookup (middle of the table)
    "lookup": """
        SELECT * FROM metrics
        WHERE timestamp = '2023-05-29 21:53:54.969619+00' AND type_id = 23;
    """
}

# assume data is in place to run benchmarks
async def benchmark(db_url: str):
    db = DatabaseSessionManager(db_url)

    results = {}

    async with db.connect() as conn:
        for name, query in QUERIES.items():
            print("Running query", name, "on", db_url)

            # separately handle range queries for now
            if name == "bucket" and db_url == settings.POSTGRES_URL:
                continue
            if name == "truncate" and db_url == settings.TIMESCALE_URL:
                continue

            result = await conn.execute(text(f"EXPLAIN (ANALYZE, FORMAT JSON) {query}"))
            data = result.fetchone()

            results[name] = data[0][0]

    await db.close()
    return results

async def main():
    # run benchmarks concurrently
    timescale_results, postgres_results = await asyncio.gather(
        benchmark(settings.TIMESCALE_URL),
        benchmark(settings.POSTGRES_URL),
    )
    
    print("===== Benchmark Results =====")

    # print results
    for query in QUERIES:


        if query == "truncate":
            continue
        elif query == "bucket":
            print("range query in TimescaleDB using time_bucket():")
            print("     Planning time: ", timescale_results["bucket"]["Planning Time"], "ms")
            print("     Execution time: ", timescale_results["bucket"]["Execution Time"], "ms")
            print("range query in Postgres using date_trunc():")
            print("     Planning time: ", postgres_results["truncate"]["Planning Time"], "ms")
            print("     Execution time: ", postgres_results["truncate"]["Execution Time"], "ms")
            print()
        else:
            print(f"{query} query in TimescaleDB:")
            print("     Planning time: ", timescale_results[query]["Planning Time"], "ms")
            print("     Execution time: ", timescale_results[query]["Execution Time"], "ms")
            print(f"{query} query in Postgres:")
            print("     Planning time: ", postgres_results[query]["Planning Time"], "ms")
            print("     Execution time: ", postgres_results[query]["Execution Time"], "ms")
            print()

if __name__ == "__main__":
    asyncio.run(main())