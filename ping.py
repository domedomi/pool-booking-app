import mysql.connector as mc
cnx = mc.connect(host="127.0.0.1", port=3306,
                 user="pb", password="pbpass",
                 database="pool_booking")
cur = cnx.cursor()
cur.execute("SELECT CURRENT_USER(), @@version, @@event_scheduler")
print(cur.fetchall())
cur.close(); cnx.close()
print("CONNECTOR_OK")
