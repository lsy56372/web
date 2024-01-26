#!/usr/bin/env python3
import cgi
import cgitb
import cx_Oracle

cgitb.enable()
form = cgi.FieldStorage()


selected_table = form.getvalue('table')
selected_attribute = form.getvalue('attribute')
selected_limit = form.getvalue('limit')

print("Content-Type: text/html\n")
print("<!DOCTYPE html>")
print("<html>")
print("<head>")
print("<title>Report</title>")
print('''<style>
        input[type="submit"] {
            
            background-color: #4CAF50; 
            color: white;
            padding: 12px 20px; 
            border: none; 
            border-radius: 4px; 
            cursor: pointer; 
            font-size: 16px; 
        }

        input[type="submit"]:hover {
            background-color: #45a049; 
        }
        .database-instructions {
    margin-top: 5px; 
    padding: 10px; 
    border: 1px solid #ccc; 
    border-radius: 5px; 
    background-color: #f9f9f9; 
}

.database-instructions h3 {
    color: #333; 
    margin-bottom: 5px; 
}

.database-instructions p {
    font-size: 1rem; 
    color: #666; 
    margin-bottom: 5px; 
}


        
    </style>''')
print("</head>")
print("<body>")
print("<h2>Database Query Interface</h2>")


print('''
<form method="get" action="https://www.geos.ed.ac.uk/~s2491874/cgi-bin/database_query.py">
    <label for="tableSelect">Choose a table:</label>
    <select name="table" id="tableSelect" multiple onchange="updateAttributes()" >
        <option value="">Select a table</option>
        <option value="Species">Species</option>
        <option value="Land_Types">Land_Types</option>
        <option value="Datazones">Datazones</option>
        <option value="Greenspaces">Greenspaces</option>
        <option value="Connectivity_Maps">Connectivity_Maps</option>
        <option value="Species_Resistance_Values">Species_Resistance_Values</option>
    </select>
    
    <br><br/>
    <label>Join Conditions(optional):</label>
    <input type="text" name="joinCondition" style="width:500px" placeholder="eg.species.species_id=species_resistance_values.species_id">
    <br></br>
    <label for="attributeSelect">Choose an attribute:</label>
    <select name="attribute" id="attributeSelect" multiple>
        <option value="">Select an attribute</option>
      
    </select>

    <label for="limitSelect">Number of records:</label>
    <select name="limit" id="limitSelect">
        <option value="5">5</option>
        <option value="10">10</option>
        <option value="15">15</option>
        <option value="30">30</option>
        <option value="100">100</option>
      
    </select>

    <input type="submit" value="Query">
</form>
<div class="database-instructions">
    <h3>How to use database query?</h3>
    <p>Step 1: Select one or more tables from the drop-down menu.(Hold Ctrl or Command to select multiple)</p>
    <p>Step 2: Enter the connection conditions (if required).If you want to query multiple tables, you need to check whether there are connection keys between the data tables.</p>
    <p>Step 3: Select the attributes you want to query.(Hold Ctrl or Command to select multiple)</p>
    <p>Step 4: Select the number of records to be returned, and then click the "Query" button.</p>
</div>
<script>
      
var tableAttributes = {
    'Species': ['SPECIES_ID', 'COMMON_NAME', 'SCIENTIFIC_NAME'],
    'Land_Types': ['TYPE_DESCRIPTION', 'LAND_TYPE_ID'],
    'Datazones': ['DATAZONE_ID', 'POPULATION', 'AREA', 'NAME'],
    'Greenspaces': ['GREENSPACE_ID', 'GREENSPACE_CODE', 'FUNCTION', 'NAME', 'AREA'],
    'Species_Resistance_Values': ['RESISTANCE_ID', 'RESISTANCE_VALUE', 'SPECIES_ID', 'LAND_TYPE_ID'],
    'Connectivity_Maps': ['MAP_ID', 'SPECIES_ID', 'METADATA', 'LAND_TYPE_ID']
    
};
function updateAttributes() {
    var tableSelect = document.getElementById('tableSelect');
    var selectedTables = [...tableSelect.selectedOptions].map(option => option.value);
    var attributeSelect = document.getElementById('attributeSelect');
    attributeSelect.innerHTML = '';  

    
    
selectedTables.forEach(function(table) {
    if (tableAttributes[table]) {
        tableAttributes[table].forEach(function(attribute) {
            var option = document.createElement('option');
            option.value = table + "." + attribute; 
            option.text = table + "." + attribute; 
            attributeSelect.appendChild(option);
        });
    }
});
}

</script>
''')



try:
    conn = cx_Oracle.connect("**************")
    c = conn.cursor()

    
    selected_tables = form.getlist('table')

    selected_attributes = ', '.join(form.getlist('attribute'))
    join_condition = form.getvalue('joinCondition')
    selected_limit = form.getvalue('limit')

    
    if selected_tables and selected_attributes and selected_limit:
        tables_clause = ', '.join(selected_tables)
        query = "SELECT {} FROM {} ".format(selected_attributes, tables_clause)
        if join_condition:
            query += "WHERE {} AND ROWNUM <= {}".format(join_condition, selected_limit)
        else:
            query += "WHERE ROWNUM <= {}".format(selected_limit)

        
        c.execute(query)
        rows = c.fetchall()

        
        if rows:
            print("<table border='1'>")
            for column_name in c.description:
                print("<th>{}</th>".format(column_name[0]))
            for row in rows:
                print("<tr>")
                for value in row:
                    print("<td>{}</td>".format(value))
                print("</tr>")
            print("</table>")
        else:
            print("<p>No results found.</p>")

except cx_Oracle.Error as e:
    print("Oracle Error:", e)

finally:
    if 'conn' in locals():
        conn.close()


print('''</body>
      </html>''')
