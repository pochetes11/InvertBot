import sqlite3 

with open('./script_para_crear_la_base_de_datos.sql', 'r') as sql_file:
    sql_script = sql_file.read()
    
    db = sqlite3.connect('tabla.db')
    cursor = db.cursor ()
    cursor.executescript(sql_script)
    db.commit()
    db.close()
