import sqlite3
import json
import os
from tkinter import E
from flask import Flask, render_template, request, redirect, jsonify
from datetime import datetime
 
app = Flask(__name__,template_folder='templates/')
 

def get_db_connection():
    conn = sqlite3.connect('isoc.db')
    conn.row_factory = sqlite3.Row
    return conn

def addDirectory(locid):
    dirname = 'static/' + str(locid)
    os.makedirs(dirname,exist_ok=True)

 
@app.route('/')
def homepage():

    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    personType = conn.execute("SELECT * FROM person_type WHERE type = 'OWNER'").fetchone()
    conn.close()
    print( personType['type_ID'])

    # conn = get_db_connection()
    # conn.row_factory = sqlite3.Row
    # locations = conn.execute('SELECT * FROM location l LEFT JOIN  history h ON h.id = ( SELECT id from history where loc_id = l.id ORDER BY date DESC LIMIT 1) ').fetchall()
    # conn.close()
    
    # data = [dict(lc) for lc in locations]
    return render_template('index.html')


@app.route('/visitors')
def vistors():

    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    visitors = conn.execute('select p.name as vname, v.vehicle_number, p.phone_number as vph, \
                        v.no_of_people, v.entry_time, v.exit_time, f.flat_no, f.bldg_no, po.name from visitor_entry v  \
                        JOIN person  p ON v.visitor_ID = p.person_ID  \
                        JOIN flat f on v.flat_ID = f.flat_ID \
                        JOIN person po ON f.owner_ID=po.person_ID').fetchall()
    conn.close()
    
    data = [dict(v) for v in visitors]
    return render_template('visitors.html',visitors = data)
    
    
@app.route('/flats')
def flats():

    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    flats = conn.execute('select * from flat f JOIN person p ON f.owner_ID =  p.person_ID  \
                                               JOIN person_type pd ON p.person_type = pd.type_ID').fetchall()
    conn.close()
    
    data = [dict(fl) for fl in flats]
    return render_template('flats.html',flats = data)

@app.route('/vehicles')
def vehicles():

    # conn = get_db_connection()
    # conn.row_factory = sqlite3.Row
    # locations = conn.execute('SELECT * FROM location l LEFT JOIN  history h ON h.id = ( SELECT id from history where loc_id = l.id ORDER BY date DESC LIMIT 1) ').fetchall()
    # conn.close()
    
    # data = [dict(lc) for lc in locations]
    return render_template('vehicles.html')   

@app.route('/settings')
def settings():

    # conn = get_db_connection()
    # conn.row_factory = sqlite3.Row
    # locations = conn.execute('SELECT * FROM location l LEFT JOIN  history h ON h.id = ( SELECT id from history where loc_id = l.id ORDER BY date DESC LIMIT 1) ').fetchall()
    # conn.close()
    
    # data = [dict(lc) for lc in locations]
    return render_template('settings.html')  

@app.route('/newvisitor')
def newvisitor():

    # conn = get_db_connection()
    # conn.row_factory = sqlite3.Row
    # locations = conn.execute('SELECT * FROM location l LEFT JOIN  history h ON h.id = ( SELECT id from history where loc_id = l.id ORDER BY date DESC LIMIT 1) ').fetchall()
    # conn.close()
    
    # data = [dict(lc) for lc in locations]
    return render_template('new-visitor.html')  


@app.route('/newvisitor', methods = ['POST'])
def createnewvisitor():
    print( request.form)

    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    personType = conn.execute("SELECT * FROM person_type WHERE type = 'VISITOR'").fetchone()
    conn.close()

    visitor_id = request.form['visitor_id']

    visting_flat_id = request.form['visting_flat_id']
    visitor_vehicle = request.form['visitor_vehicle']
    visting_count = request.form['visting_count']
     
    if( len(visitor_id) == 0):
        conn = get_db_connection()
        cursor = conn.cursor()
        rec = cursor.execute("INSERT INTO person (name, phone_number, person_type) VALUES (?,?,?)",
                    [request.form['person_name'], request.form['person_phone'], personType['type_ID']]
                    )
    
        visitor_id = rec.lastrowid;
        print(  rec.lastrowid)
        rec2 = conn.commit()
        print( rec2)
        conn.close()

    

    entry = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    error = ''
    try:
        newFlat = cursor.execute("INSERT INTO visitor_entry (visitor_ID, flat_ID, entry_time,vehicle_number,no_of_people) VALUES (?,?,?,?,?)",
                    [ visitor_id, visting_flat_id, entry, visitor_vehicle , visting_count]
                    )
    except sqlite3.IntegrityError:
        error='Record already exists in database!'
        return render_template('new-flat.html', error=error)

    person_id = newFlat.lastrowid;
    print( newFlat.lastrowid)
    rec2 = conn.commit()

    return render_template('index.html')  

@app.route('/newflat')
def newflat():

    # conn = get_db_connection()
    # conn.row_factory = sqlite3.Row
    # locations = conn.execute('SELECT type_ID FROM person_type WHERE type like '?' ').fetchall()
    # conn.close()
    
    # data = [dict(lc) for lc in locations]
    return render_template('new-flat.html', error='')  


@app.route('/newflat', methods = ['POST'])
def createnewflat():
  
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    personType = conn.execute("SELECT * FROM person_type WHERE type = 'OWNER'").fetchone()
    conn.close()
    
    print(  request.form);
    person_id = request.form['owner_id']
    print( 'person_id is ' + person_id)
    if( len(person_id) == 0):
        conn = get_db_connection()

        cursor = conn.cursor()
        rec = cursor.execute("INSERT INTO person (name, phone_number, person_type) VALUES (?,?,?)",
                    [request.form['owner_name'], request.form['owner_phone'], personType['type_ID']]
                    )
    
        person_id = rec.lastrowid;
        print(  rec.lastrowid)
        rec2 = conn.commit()
        print( rec2)
        conn.close()


    print(   person_id)



    conn = get_db_connection()
    cursor = conn.cursor()
    error = ''
    try:
        newFlat = cursor.execute("INSERT INTO flat (flat_no, bldg_no, floor_no,area,owner_ID) VALUES (?,?,?,?,?)",
                    [request.form['flat_no'], request.form['building_no'], request.form['floor'],request.form['area'],person_id ]
                    )
    except sqlite3.IntegrityError:
        error='Record already exists in database!'
        return render_template('new-flat.html', error=error)

    person_id = newFlat.lastrowid;
    print( newFlat.lastrowid)
    rec2 = conn.commit()



    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    flats = conn.execute('select * from flat f JOIN person p ON f.owner_ID =  p.person_ID  \
                                               JOIN person_type pd ON p.person_type = pd.type_ID').fetchall()
    conn.close()
    
    data = [dict(fl) for fl in flats]
    return render_template('flats.html',flats = data , error=error)

@app.route('/person/owner' )
def getownerlist():

    name = request.args['query']
    name = '%'+name+'%'
    print( name)
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    owners = conn.execute("select * from person p JOIN flat f ON p.person_ID = f.owner_ID WHERE ( p.person_type == 1 OR p.person_type == 2 ) AND p.name like ? ",[name]).fetchall()
    conn.close()

    data = [dict(lc) for lc in owners]
    print (data)

    return data


@app.route('/person/visitor' )
def getvisitorlist():

    phno = request.args['query']
    phno = '%'+phno+'%'
    print( phno)
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    owners = conn.execute("select * from person p WHERE p.person_type == 3 AND p.phone_number like ? ",[phno]).fetchall()
    conn.close()

    data = [dict(lc) for lc in owners]
    print (data)

    return data



if __name__ == '__main__':
    app.run(debug=True)

