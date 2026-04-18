#!/usr/bin/python3
import MySQLdb
import sys
import requests

# Disable warnings from urllib3
requests.packages.urllib3.disable_warnings()

# Check for exactly one argument
if len(sys.argv) != 2:
    print("Please pass only one argument. E.G. script.py something")
    sys.exit()

# Connect to the MySQL database
try:
    conn = MySQLdb.connect(host="10.0.254.101", user="check", passwd="check", db="hyvetest")
except MySQLdb.Error as e:
    print(f"Error connecting to the database: {e}")
    sys.exit()

cursor = conn.cursor()

# Prepare and execute the SQL query with a placeholder for the argument
try:
    query = """
    SELECT 
        Server.sn_tag, 
        ServerStatus.server_id, 
        ServerStatus.started, 
        ServerStatus.finished, 
        ServerStatus.ok 
    FROM 
        Server, 
        ServerStatus 
    WHERE 
        ServerStatus.server_id = Server.id 
        AND Server.sn_tag = %s 
    ORDER BY 
        ServerStatus.id DESC 
    LIMIT 1;
    """
    cursor.execute(query, (sys.argv[1],))
    row = cursor.fetchall()

    # Check if any results are returned
    if row:
        for r in row:
            print(f"SN Tag: {r[0]}, Server ID: {r[1]}, Started: {r[2]}, Finished: {r[3]}, OK: {r[4]}")
    else:
        print("No matching records found.")

except MySQLdb.Error as e:
    print(f"Error executing query: {e}")
finally:
    # Close the cursor and connection
    cursor.close()
    conn.close()