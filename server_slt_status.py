#!/usr/bin/python3
import MySQLdb
import sys
import requests
# Disable warnings from urllib3
requests.packages.urllib3.disable_warnings()
# Check for exactly one argument
if len(sys.argv) != 2:
   print("Please pass exactly one argument. E.g., script.py something")
   sys.exit(1)
sn_tag = sys.argv[1]
try:
   # Establish database connection
   conn = MySQLdb.connect(host="10.0.254.101", user="check", passwd="check", db="hyvetest")
   cursor = conn.cursor()
   # Execute the query with parameterized input
   query = """
   SELECT Server.sn_tag, ServerStatus.server_id, ServerStatus.started, ServerStatus.finished, ServerStatus.ok
   FROM Server
   JOIN ServerStatus ON ServerStatus.server_id = Server.id
   WHERE Server.sn_tag = %s
   ORDER BY ServerStatus.id DESC
   LIMIT 1;
   """
   cursor.execute(query, (sn_tag,))
   # Fetch and print the result
   row = cursor.fetchone()
   if row:
       print(row)
   else:
       print("No results found.")
except MySQLdb.Error as e:
   print(f"Error connecting to MySQL database: {e}")
finally:
   # Ensure the connection is closed
   if conn:
       conn.close()