from pathlib import Path
import duckdb

DB_PATH = Path(
    r"D:\Project_Lighthouse\projects\P0_Data_Platform\datasets\lendingclub\data\warehouse\duckdb\lendingclub.duckdb"
)

conn = duckdb.connect(str(DB_PATH))

outfile = Path(
    r"D:\Project_Lighthouse\duckdb_inventory.txt"
)

with open(outfile, "w", encoding="utf-8") as f:

    f.write("DATABASE INVENTORY\n\n")

    tables = conn.execute("""
        select
            table_schema,
            table_name
        from information_schema.tables
        order by 1,2
    """).fetchall()

    for schema, table in tables:

        f.write(f"\n{'='*80}\n")
        f.write(f"{schema}.{table}\n")
        f.write(f"{'='*80}\n")

        try:
            count = conn.execute(
                f"select count(*) from {schema}.{table}"
            ).fetchone()[0]

            f.write(f"ROWS: {count}\n\n")

        except:
            pass

        desc = conn.execute(
            f"describe {schema}.{table}"
        ).fetchdf()

        f.write(desc.to_string())
        f.write("\n")

conn.close()

print(outfile)