import psycopg2

connection = psycopg2.connect('postgresql://neondb_owner:npg_r7DAfQCj5Hpz@ep-patient-poetry-aywk2n7c-pooler.c-5.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require')

def main():
    
    try:
        cursor = connection.cursor()

        # Execute the SELECT query
        cursor.execute("SELECT * FROM checkpoints;")

        # Fetch all returned rows
        rows = cursor.fetchall()

        # Loop through and print each row
        for row in rows:
            print(f"C_ID: {row[0]}, State: {row[1]},  Config: {row[2]}")

    except Exception as error:
        print("Error fetching data:", error)

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection:
            connection.close()


main()