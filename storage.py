import sqlite3

def create_transcriptions_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transcriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            source_url TEXT,
            transcription TEXT,
            summary TEXT,
            issue_category TEXT
        )
    ''')
    conn.commit()

def store_transcription_in_sqlite(source_url, transcription, date, summary, issue_category, db_path='transcriptions.db'):
    # Connect to SQLite database
    conn = sqlite3.connect(db_path)

    # Create transcriptions table if not exists
    create_transcriptions_table(conn)

    # Insert data into the transcriptions table
    conn.execute('''
        INSERT INTO transcriptions (source_url, transcription, date, summary, issue_category)
        VALUES (?, ?, ?, ?, ?)
    ''', (source_url, transcription, date, summary, issue_category))

    # Commit changes and close the connection
    conn.commit()
    conn.close()
