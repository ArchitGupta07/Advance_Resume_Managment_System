import psycopg2 as pg

try:
    conn = pg.connect(
        host='dpg-co746oed3nmc73e3p320-a.singapore-postgres.render.com',
        database='resumemanagement',
        port=5432,
        user='root',
        password='qvQ0SgoOHhN4sd5pcLMpwqZkuobAhEDS'
    )

    cursor = conn.cursor()
    print("Connection established.")

    # try:
    #     cursor.execute("CREATE TABLE IF NOT EXISTS test (id serial PRIMARY KEY, num integer, data varchar);")
    #     print("Table created successfully.")
    # except Exception as create_err:
    #     print("Error creating table:", create_err)

    # # Add records
    # try:
    #     cursor.execute("INSERT INTO test (num, data) VALUES (1, 'First row');")
    #     cursor.execute("INSERT INTO test (num, data) VALUES (2, 'Second row');")
    #     cursor.execute("INSERT INTO test (num, data) VALUES (3, 'Third row');")
    #     print("Records inserted successfully.")
    #     conn.commit()
    # except Exception as insert_err:
    #     print("Error inserting records:", insert_err)

    # Fetch records
    # try:
    #     cursor.execute("SELECT * FROM test;")
    #     records = cursor.fetchall()
    #     print("\nRecords in the table:")
    #     for row in records:
    #         print(row)
    # except Exception as fetch_err:
    #     print("Error fetching records:", fetch_err)

    # cursor.close()
    # conn.close()

except Exception as err:
    print("Something went wrong.")
    print(err)