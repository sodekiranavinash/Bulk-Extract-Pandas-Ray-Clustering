import mysql.connector
import random
import string

def chunked_insert(cursor, table_name, data, chunk_size=1000):
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i+chunk_size]
        cursor.executemany(f'''
            INSERT INTO {table_name} (first_name, last_name, email, department, salary)
            VALUES (%s, %s, %s, %s, %s)
        ''', chunk)

def main():
    try:
        # Connect to the MySQL database
        conn = mysql.connector.connect(
            host="localhost",
            user="avinash",
            password="avinash123",
            database="ray_clustering"
        )

        table_name = "employee_info"

        # Create a cursor object
        cursor = conn.cursor()

        # Sample data for employees
        departments = ['Engineering', 'Marketing', 'HR', 'Finance', 'Sales']
        employees_data = []

        # Generate ten million rows of sample data
        for i in range(1, 1000001):
            first_name = ''.join(random.choices(string.ascii_uppercase, k=5))
            last_name = ''.join(random.choices(string.ascii_uppercase, k=5))
            email = f'{first_name.lower()}.{last_name.lower()}@example.com'
            department = random.choice(departments)
            salary = random.randint(50000, 100000)
            employees_data.append((first_name, last_name, email, department, salary))

        # Create the table if it doesn't exist
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(255),
                last_name VARCHAR(255),
                email VARCHAR(255),
                department VARCHAR(255),
                salary FLOAT
            )
        ''')

        # Insert data in smaller chunks
        chunked_insert(cursor, table_name, employees_data)

        # Commit the transaction
        conn.commit()

        print("Data inserted successfully.")

    except mysql.connector.Error as e:
        print("Error connecting to the database:", e)

    finally:
        # Close the cursor and connection
        if conn is not None and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    main()
