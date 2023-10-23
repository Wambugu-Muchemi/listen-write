import sqlite3

def create_transcriptions_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transcriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_url TEXT,
            transcription TEXT
        )
    ''')
    conn.commit()

def store_transcription_in_sqlite(source_url, transcription, db_path='transcriptions.db'):
    # Connect to SQLite database
    conn = sqlite3.connect(db_path)

    # Create transcriptions table if not exists
    create_transcriptions_table(conn)

    # Insert data into the transcriptions table
    conn.execute('''
        INSERT INTO transcriptions (source_url, transcription)
        VALUES (?, ?)
    ''', (source_url, transcription))

    # Commit changes and close the connection
    conn.commit()
    conn.close()
