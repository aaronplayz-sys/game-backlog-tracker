from database import DatabaseManager

def load_samples():
    db = DatabaseManager()
    db.connect()
    db.create_tables()

    with open("sample_data.sql", "r") as f:
        sql = f.read()

    # Filter out comments and blank lines, then execute each statement
    statements = [
        line.strip() for line in sql.splitlines()
        if line.strip() and not line.strip().startswith("--")
    ]

    cursor = db.get_connection().cursor()
    for statement in statements:
        cursor.execute(statement)

    db.get_connection().commit()
    print(f"Sample data loaded successfully! ({len(statements)} records inserted)")
    db.disconnect()

if __name__ == "__main__":
    load_samples()