import psycopg2
import os

# Update these with your PostgreSQL credentials
DB_NAME = "call_summaries"
DB_USER = "postgres"
DB_PASSWORD = os.environ.get("PGPASSWORD")
DB_HOST = "localhost"
DB_PORT = "5432"

def create_table():
    create_table_query = """
    CREATE TABLE IF NOT EXISTS call_summaries (
        id SERIAL PRIMARY KEY,
        customer_name TEXT,
        agent_name TEXT,
        call_date DATE,
        call_duration TEXT,
        conversation_highlights TEXT[],
        action_items JSONB,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER,
            password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
        )
        cursor = conn.cursor()
        cursor.execute(create_table_query)
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Table 'call_summaries' created (or already exists).")
    except Exception as e:
        print("❌ Error during schema migration:", e)

if __name__ == "__main__":
    create_table()
