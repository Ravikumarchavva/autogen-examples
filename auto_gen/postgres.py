from mcp.server.fastmcp import FastMCP
from typing import Any
from sqlalchemy import create_engine, text

def get_db_connection():
    connection_string = "postgresql://postgres:postgres@localhost:5432/postgres"
    engine = create_engine(connection_string)
    return engine.connect()     

def execute_query(query):
    connection = get_db_connection()
    try:
        result = connection.execute(text(query))
        return result.fetchall()
    finally:
        connection.close()

execute_query("SELECT * FROM public.testgg;")

mcp = FastMCP("postgres")

@mcp.tool()
def get_postgres_data(query: str) -> Any:
    """
    Fetch data from PostgreSQL database.

    Args:
        query (str): SQL query to execute.

    Returns:
        Any: Query result or error message.
    """
    try:
        result = execute_query(query)
        return result
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run(transport="stdio")
