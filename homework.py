from sqlalchemy import create_engine, text

# Database engine
engine = create_engine("sqlite:///example2.db", echo=True)

# Connection
with engine.connect() as ras:
#user2 table
    ras.execute(text("""
        CREATE TABLE IF NOT EXISTS user2 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            address TEXT
        )
    """))

# user3 table
    ras.execute(text("""
        CREATE TABLE IF NOT EXISTS user3 (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          project_name TEXT,
          intern_id  INTEGER,
          FOREIGN KEY (intern_id) REFERENCES user2 (id)
        )
    """))

    try:
        ras.execute(text("ALTER TABLE user2 ADD COLUMN email TEXT"))
    except Exception as a:
        print(f"Warning: {a}")

    try:
        ras.execute(text("ALTER TABLE user2 RENAME TO interns"))
    except Exception as b:
        print(f"Warning: {b}")


    # Table 1
    ras.execute(text("INSERT INTO user2 (name, age, address, email) VALUES ('Darshan', 22, 'Lalbagh Road', 'd@email.com')"))
    ras.execute(text("INSERT INTO user2 (name, age, address, email) VALUES ('Prajwal', 23, 'BTM', 'p@email.com')"))
    ras.execute(text("INSERT INTO user2 (name, age, address, email) VALUES ('Shivu', 24, 'Nagarbhavi', 's@email.com')"))
    ras.execute(text("INSERT INTO user2 (name, age, address, email) VALUES ('Sanjay', 22, 'BTM','s@email.com')"))
    ras.execute(text("INSERT INTO user2 (name, age, address, email) VALUES ('Mayur', 22, 'DoddaKallasandra','m@email.com')"))

    # Table 2
    ras.execute(text("INSERT INTO user3 (project_name, intern_id) VALUES ('Schreiber Foods', 1)"))
    ras.execute(text("INSERT INTO user3 (project_name, intern_id) VALUES ('Learning', 1)"))
    ras.execute(text("INSERT INTO user3 (project_name, intern_id) VALUES ('Schreiber Foods', 2)"))
    ras.execute(text("INSERT INTO user3 (project_name, intern_id) VALUES ('Schreiber Foods', 3)"))
    ras.execute(text("INSERT INTO user3 (project_name, intern_id) VALUES ('Learning', 3)"))
    ras.execute(text("INSERT INTO user3 (project_name, intern_id) VALUES ('Schreiber Foods', 4)"))

    # Query data
    result = ras.execute(text("SELECT * FROM user3"))
    # Fetch all rows
    for row in result:
        print(row)


    result = ras.execute(text("SELECT * FROM user2"))
    for row in result:
        print(row)


    #Joins
    #Matching values in both tables
    result = ras.execute(text("""
            SELECT user2.name, user3.project_name
            FROM user2
            INNER JOIN user3 ON user2.id = user3.intern_id
        """))
    for row in result:
        print(row)


    #Left Joins
    #If there is no match, it returns NULL on the side of the right table
    result = ras.execute(text("""
            SELECT user2.name, user3.project_name
            FROM user2
            LEFT JOIN user3 ON user2.id = user3.intern_id
        """))
    for row in result:
        print(row)


    #SQLite does not support Right Join directly
    #Right Join, you can use a Left Join with the tables in the reverse order
    #Full outer Join, match in either left or right table records


    #Update
    # ras.execute(text("UPDATE user2 SET address = 'New Address' WHERE name = 'Darshan'"))
    # result = ras.execute(text("SELECT * FROM user2"))
    # for row in result:
    #  print(row)


    #Delete
    # ras.execute(text("DELETE FROM user2 WHERE name = 'Darshan'"))
    # result = ras.execute(text("SELECT * FROM user2"))
    # for row in result:
    #     print(row)


    #Drop
    # Create a new table without the 'email' column
    # Copy data from the old table to the new table
    # Drop the old table


    #Sub-Query
    result = ras.execute(text("""
            SELECT name
            FROM user2
            WHERE id IN (
                SELECT intern_id
                FROM user3
                WHERE project_name = 'Schreiber Foods'
            )
        """))
    for row in result:
      print(row)

   #Nested - subquery that appears within another subquery
    result = ras.execute(text("""
        SELECT name
        FROM user2
        WHERE id IN (
            SELECT intern_id
            FROM user3
            WHERE project_name IN (
                SELECT project_name
                FROM user3
                WHERE project_name LIKE '%Foods%'
            )
        )
    """))
    for row in result:
     print(row)


   #Aggregate Functions

    #COUNT
    result_count = ras.execute(text("SELECT COUNT(*) AS total_interns FROM user2"))
    total_interns_count = result_count.fetchone()[0]
    print(f"Total number of interns: {total_interns_count}")

    #AVG
    result = ras.execute(text("SELECT AVG(age) AS average_age FROM user2"))
    average_age = result.fetchone()[0]
    print(f"Average age of interns: {average_age}")

    #MIN
    result = ras.execute(text("SELECT MIN(age) AS minimum_age FROM user2"))
    minimum_age = result.fetchone()[0]
    print(f"Minimum age of interns: {minimum_age}")

    #MAX
    result = ras.execute(text("SELECT MAX(age) AS maximum_age FROM user2"))
    maximum_age = result.fetchone()[0]
    print(f"Maximum age of interns: {maximum_age}")



    #Order By

    #Ascending order
    result_ascending = ras.execute(text("SELECT * FROM user2 ORDER BY age ASC"))
    for row in result_ascending:
     print(row)

    #Descending order
    result_descending = ras.execute(text("SELECT * FROM user2 ORDER BY age DESC"))
    for row in result_descending:
     print(row)
