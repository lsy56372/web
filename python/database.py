#!/usr/bin/env python3
import cgi
import cgitb
import cx_Oracle

cgitb.enable()

print("Content-Type: text/html\n")
print("<!DOCTYPE html>")
print("<html>")
print("<head>")
print("<title>Report</title>")
print("</head>")
print("<body>")
print("<h2>Database</h2>")
print("<h3>Database Table</h3>")

# Define a list of table names
table_names = ["Species", "Land_Types", "Species_Resistance_Values", "Greenspaces", "Connectivity_Maps", "Datazones"]

try:
    conn = cx_Oracle.connect("s2491874/s2491874@geoslearn")
    c = conn.cursor()

    for table_name in table_names:
        # Wrap the table name in a link
        print("<h4><a href='#' onclick='toggleTable(\"{}\")'>{}</a></h4>".format(table_name, table_name))
        
        # Assuming each table has at least two columns
        if table_name == "Greenspaces":
            # Add ORDER BY greenspace_ID to sort Greenspaces table by greenspace_ID in ascending order
            c.execute("SELECT * FROM {} ORDER BY greenspace_ID".format(table_name))
        elif table_name == "Datazones":
            # Add ORDER BY datazone_id to sort Datazones table by datazone_id in ascending order
            c.execute("SELECT * FROM {} ORDER BY datazone_id".format(table_name))
        else:
            c.execute("SELECT * FROM {}".format(table_name))

        # Fetch all rows at once
        rows = c.fetchall()

        # Check if there are any rows
        if rows:
            # Print table content with a specific ID for toggling visibility
            print("<table id='{}' border='1' style='display:none'>".format(table_name))
            print("<tr>")
            for column_name in c.description:
                print("<th>{}</th>".format(column_name[0]))
            print("</tr>")

            # Print table rows
            for row in rows:
                print("<tr>")
                for value in row:
                    print("<td>{}</td>".format(value))
                print("</tr>")
            
            print("</table>")
        else:
            print("<p>No data found for table {}.</p>".format(table_name))

except cx_Oracle.Error as e:
    print("Oracle Error:", e)

finally:
    if 'conn' in locals():
        conn.close()

# JavaScript function for toggling table visibility
print('''
<script>
function toggleTable(tableId) {
    var table = document.getElementById(tableId);
    if (table.style.display === 'none') {
        table.style.display = 'table';
    } else {
        table.style.display = 'none';
    }
}
</script>
''')

print('''</body>
      </html>''')
