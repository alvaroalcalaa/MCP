from __future__ import annotations

import os
import sqlite3
from pathlib import Path
import pandas as pd

from mcp.server.fastmcp import FastMCP

# =========================
# CONFIG
# =========================
mcp = FastMCP("sales-mcp-demo", json_response=True)

BASE_DIR = Path(__file__).parent
CSV_PATH = BASE_DIR / "sales.csv"

conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row

# =========================
# LOAD DATA
# =========================
df = pd.read_csv(CSV_PATH)
df["date"] = pd.to_datetime(df["date"])
df["revenue"] = df["price"] * df["quantity"] * (1 - df["discount"])

df.to_sql("sales", conn, index=False, if_exists="replace")

# =========================
# RESOURCES
# =========================
@mcp.resource("sales://data")
def sales_data():
    return df.to_csv(index=False)

@mcp.resource("sales://schema")
def sales_schema():
    return "\n".join([f"{c}: {t}" for c, t in df.dtypes.items()])

# =========================
# TOOLS
# =========================
@mcp.tool()
def monthly_revenue():
    temp = df.copy()
    temp["month"] = temp["date"].dt.to_period("M").astype(str)
    result = temp.groupby("month")["revenue"].sum().reset_index()
    return result.to_string(index=False)

@mcp.tool()
def summary_stats():
    return f"""
Revenue total: {df['revenue'].sum():.2f}
Pedidos: {df['order_id'].nunique()}
"""

@mcp.tool()
def query_sales(sql: str):
    try:
        result = pd.read_sql_query(sql, conn)
        return result.to_string(index=False)
    except Exception as e:
        return str(e)

# =========================
# DEMO MODE
# =========================
def run_demo():
    print("🚀 MCP SALES DEMO")
    print()

    print("🔹 Tools disponibles:")
    print("- monthly_revenue()")
    print("- summary_stats()")
    print("- query_sales(sql)")
    print()

    print("🔹 Simulación:")
    print("summary_stats()")
    print(summary_stats())
    print()

    print("monthly_revenue()")
    print(monthly_revenue())
    print()

    print("🧠 EXPLICACIÓN:")
    print("Sin MCP → código hardcodeado")
    print("Con MCP → el modelo decide qué tool usar")

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    if os.getenv("MCP_DEMO") == "1":
        run_demo()
    else:
        mcp.run(transport="stdio")