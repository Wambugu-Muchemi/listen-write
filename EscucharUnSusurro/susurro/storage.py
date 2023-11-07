import sqlite3

TABLE_NAME = 'transcriptions'

def create_transcriptions_table(conn, table_name):
    """
    Create the transcriptions table if it doesn't exist.

    Args:
    - conn: The SQLite database connection.
    - table_name: The name of the transcriptions table.
    """
    cursor = conn.cursor()
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            source_url TEXT,
            transcription TEXT,
            summary TEXT,
            issue_category TEXT,
            contact TEXT
        )
    ''')
    conn.commit()

def store_transcription_in_sqlite(source_url, transcription, date, summary, issue_category, contact, db_path='transcriptions.db'):
    """
    Store transcription data in SQLite database.

    Args:
    - source_url: The source URL.
    - transcription: The transcription text.
    - date: The date of the transcription.
    - summary: The summary of the transcription.
    - issue_category: The issue category.
    - contact: The customer contact information.
    - db_path: The path to the SQLite database file.
    """
    try:
        # Connect to SQLite database
        with sqlite3.connect(db_path) as conn:

            # Create transcriptions table if not exists
            create_transcriptions_table(conn, TABLE_NAME)

            # Insert data into the transcriptions table
            conn.execute(f'''
                INSERT INTO {TABLE_NAME} (source_url, transcription, date, summary, issue_category, contact)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (source_url, transcription, date, summary, issue_category, contact))

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

    except Exception as e:
        print(f"Error storing transcription in SQLite: {e}")

