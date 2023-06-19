import cx_Oracle
from ldap3 import Server, Connection, ALL, MODIFY_REPLACE

# Connect to Oracle DB
dsn_tns = cx_Oracle.makedsn('<hostname>', '<port>', service_name='<service_name>') 
conn = cx_Oracle.connect(user='<username>', password='<password>', dsn=dsn_tns) 

c = conn.cursor()
c.execute("SELECT * FROM employees")  # replace with your query

# Connect to Active Directory
server = Server('<ldap_server>', get_info=ALL)
conn_ad = Connection(server, user='<username>', password='<password>')

if not conn_ad.bind():
    print('Error in bind', conn_ad.result)
else:
    for row in c:
        # Assuming the table has columns: 'id', 'name', 'email'
        employee_id, name, email = row

        # Define the DN of the user
        dn = "cn={},ou=users,dc=example,dc=com".format(name)  # replace with your DN

        # Check if the user exists
        conn_ad.search(search_base=dn, search_filter='(objectClass=person)', search_scope='BASE')
        if conn_ad.response:
            # The user exists, check if any details have been modified
            user = conn_ad.response[0]['attributes']

            modifications = {}
            if user['sAMAccountName'] != employee_id:
                modifications['sAMAccountName'] = [(MODIFY_REPLACE, [employee_id])]
            if user['userPrincipalName'] != email:
                modifications['userPrincipalName'] = [(MODIFY_REPLACE, [email])]

            # If any details have been modified, update the user
            if modifications:
                conn_ad.modify(dn, modifications)

conn_ad.unbind()
conn.close()
