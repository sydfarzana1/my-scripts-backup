#!/usr/bin/env python3

import MySQLdb
import sys

def mysqlconnect():
    try:
        # Establish a connection to the database
        db_connection = MySQLdb.connect(
            host="10.0.254.101", 
            user="qc_read_only", 
            passwd="rX9jC8oW2pK1iL3x", 
            db="hyvetest"
        )
    except MySQLdb.Error as e:
        print(f"Can't connect to database: {e}")
        return

    print("Connected")

    cursor = db_connection.cursor()

    # Use sys.argv to get the input from the command line
    if len(sys.argv) < 2:
        print("Please provide a project name.")
        return
    project_name = sys.argv[1]

    # Define the query with a placeholder
    query = "SELECT id, name FROM Project WHERE name REGEXP %s"

    try:
        # Execute the query with the project name provided as an argument
        cursor.execute(query, (project_name,))
        results = cursor.fetchall()

        # Print the results
        if results:
            for row in results:
                print(row)
        else:
            print("No matching projects found.")

    except MySQLdb.Error as e:
        print(f"Error executing query: {e}")

    finally:
        # Close the cursor and connection
        cursor.close()
        db_connection.close()

if __name__ == "__main__":
    mysqlconnect()