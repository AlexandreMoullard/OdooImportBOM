#Importation of a product in the database
"""
Todo :
	- Add the date of creation of each line (in the database table)
	- Add the supplier and manufacturer references & id
	- Import from an external file the connection string
	- Check if name or suppliers or manufacturer references are not allready existing + alert message if yes 
"""

import csv
import psycopg2
import sys

conn_string = "dbname='bitnami_openerp' user='bn_openerp' password='08de99d3' host='127.0.0.1'"
conn = psycopg2.connect(conn_string)

cursor = conn.cursor()

with open('products.csv', 'r') as f:
    reader = csv.reader(f, delimiter=';')
    for row in reader :
        print (row[1])
    
        #import routine
        statement = "INSERT INTO product_template(name,warranty,list_price,mes_type,weight,write_uid,uos_coeff,create_uid,company_id,uom_id,uom_po_id,type,weight_net,volume,active,rental,track_all,track_outgoing,track_incoming,sale_delay,track_production,produce_delay,categ_id,sale_ok) VALUES ('"+ row[1] + "',0," + str(row[2])  +",'fixed',0.00,1,1.000,1,1,1,1,'product',0.00,0,TRUE,FALSE,FALSE,FALSE,FALSE,7,FALSE,1,1,True) RETURNING id"

        cursor.execute(statement)
        conn.commit()
        templateid = cursor.fetchone()[0]
    
        statement = "INSERT INTO product_product (product_tmpl_id,default_code,active) VALUES \
        (" + str(templateid) + ",'" + row[0] + "',TRUE)"
    
        cursor.execute(statement)
        conn.commit()
