#Importation of a product in the database

#Template imported in database:
#row[0] seller's product name  
#row[1] name of the product (intern)
#row[2] price of the product
#row[3] seller's name
#row[4] seller's product code
#Create a new line for each seller, keep the same name

"""
Todo :
	- Add the supplier and manufacturer references & id
	- Check if name or suppliers or manufacturer references are not allready existing + alert message if yes 
"""

import csv
import psycopg2
import sys
import datetime

#Giving a timestamp to imported products
time = datetime.datetime.now()

#Login to server using an external file called "login"
#This file has to contain:"dbname='xxx' user='xxx' password='xxx' host='xxx'" (replace xxx with correct values)
myfile = open ("login", "r")
conn_string = myfile . read ()
print(conn_string)
myfile . close ()

conn = psycopg2.connect(conn_string)

cursor = conn.cursor()

with open('products.csv', 'r') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader :
        print (row[1])
    
        #import routine product_template
        statement = "INSERT INTO product_template(name,warranty,list_price,mes_type,weight,write_uid,uos_coeff,create_uid,company_id,uom_id,uom_po_id,type,weight_net,volume,active,rental,track_all,track_outgoing,track_incoming,sale_delay,track_production,produce_delay,categ_id,sale_ok,create_date,write_date) VALUES ('"+ row[1] + "',0," + str(row[2])  +",'fixed',0.00,1,1.000,1,1,1,1,'product',0.00,0,TRUE,FALSE,FALSE,FALSE,FALSE,7,FALSE,1,1,True,'"+ str(time) +"','"+ str(time) +"') RETURNING id"

        cursor.execute(statement)
        conn.commit()
        templateid = cursor.fetchone()[0]
	print(templateid)

	#import routine product_supplierinfo
	#retrieves the supplier id
	cursor.execute("SELECT id FROM res_partner WHERE name='"+ row[3] +"'")
	supplierid = cursor.fetchone()[0]
	print(supplierid)

	statement = "INSERT INTO product_supplierinfo(create_uid,product_code,create_date,name,sequence,product_name,company_id,write_uid,delay,write_date,min_qty,qty,product_tmpl_id) VALUES (1,'"+ row[4] +"','"+ str(time) +"','"+ str(supplierid) +"',1,'"+ row[0] + "',1,1,1,'"+ str(time) +"',0,0.00,'"+ str(templateid) +"')"

        cursor.execute(statement)
        conn.commit()
    
	#import routine product_product -> issue, has to be corrected
	#replace by  (create_date,name_template,create_uid,product_tmpl_id,write_uid,write_date,active)        
	statement = "INSERT INTO product_product (product_tmpl_id,default_code,active) VALUES \
        (" + str(templateid) + ",'" + row[0] + "',TRUE)"
    
        cursor.execute(statement)
        conn.commit()
