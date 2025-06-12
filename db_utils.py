import psycopg2
from psycopg2.extras import Json
from datetime import datetime
import os

# Database connection settings (read password from environment variable for security)
DB_NAME = "call_summaries"
DB_USER = "postgres"
DB_PASSWORD = os.environ.get("PGPASSWORD")
DB_HOST = "localhost"
DB_PORT = "5432"

def save_summary_to_db(summary_dict):
    """
    Save a call summary dictionary to the PostgreSQL database.

    Args:
        summary_dict (dict): The summary data to save.
    """
    try:
        # Establish database connection
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = conn.cursor()

        # Extract and prepare values from the summary dictionary
        customer_name = summary_dict["call_info"].get("customer_name", "")
        agent_name = summary_dict["call_info"].get("agent_name", "")
        call_date_str = summary_dict["call_info"].get("date", "")
        # Parse date string if present, else set to None
        call_date = datetime.strptime(call_date_str, "%Y-%m-%d").date() if call_date_str else None
        call_duration = summary_dict["call_info"].get("duration", "")
        highlights = summary_dict.get("conversation_highlights", [])
        action_items = summary_dict.get("action_items", [])

        # SQL Insert statement for the call_summaries table
        insert_query = """
        INSERT INTO call_summaries (
            customer_name,
            agent_name,
            call_date,
            call_duration,
            conversation_highlights,
            action_items
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        # Execute the insert with the prepared values
        cursor.execute(
            insert_query,
            (
                customer_name,
                agent_name,
                call_date,
                call_duration,
                highlights,
                Json(action_items)
            )
        )

        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Summary successfully saved to database.")

    except Exception as e:
        # Print error if saving fails
        print("❌ Failed to save summary:", e)
