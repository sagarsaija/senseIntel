import sqlite3

def read_from_database():
    """Read data from the database and print it."""
    try:
        conn = sqlite3.connect('serial_data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM serial_data')
        rows = cursor.fetchall()
        if rows:
            print("Data from database:")
            for row in rows:
                print(row)
        else:
            print("No data in the database.")
    except sqlite3.Error as e:
        print("Error reading from the database:", e)
    finally:
        conn.close()

def main():
    read_from_database()

if __name__ == "__main__":
    main()

