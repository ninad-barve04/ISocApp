import sqlite3
import json
import os
from tkinter import E
from flask import Flask, render_template, request, redirect, jsonify
from datetime import datetime
from werkzeug.utils import secure_filename
import visitors
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
    vehicles = conn.execute('select count(*) as veh_count from vehicle').fetchall()
    flats = conn.execute('select count(*) as flat_count from flat').fetchall()
    visitors = conn.execute('select count(*) as visitor_count from visitor_entry').fetchall()
    socList = conn.execute('select *  from society').fetchall()
    conn.close()

    data = [dict(v) for v in socList]


    veh_count = (vehicles[0]['veh_count'] )
    flat_count = (flats[0]['flat_count'])
    visitor_count = (visitors[0]['visitor_count'])

    return render_template('index.html', society=data[0],veh_count=veh_count, flat_count=flat_count, visitor_count=visitor_count )


@app.route('/visitors')
def vistors():

    # conn = get_db_connection()
    # conn.row_factory = sqlite3.Row
    # visitors = conn.execute('SELECT p.name AS vname, v.vehicle_number, p.phone_number AS vph, \
    #                     v.no_of_people, v.entry_time, v.exit_time, f.flat_no, f.bldg_no, po.name FROM visitor_entry v  \
    #                     JOIN person  p ON v.visitor_ID = p.person_ID  \
    #                     JOIN flat f ON v.flat_ID = f.flat_ID \
    #                     JOIN person po ON f.owner_ID=po.person_ID').fetchall()
    # conn.close()

    #print( request.args['all'])

    visitorList = visitors.getVisitors("0");
    
    data = [dict(v) for v in visitorList]
    print(data)
    return render_template('visitors.html',visitors = data, inpremise=1)
    
    
@app.route('/flats')
def flats():

    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    # flats = conn.execute('SELECT * FROM flat f JOIN flat_owner_history_table fo ON f.flat_ID = fo.flat_ID \
    #                                 JOIN flat_occupant_table ft ON f.flat_ID = ft.flat_ID \
    #                                 JOIN person po ON ft.occupant_ID=po.person_ID ').fetchall()


    flats = conn.execute("""
                            SELECT * FROM flat fl JOIN (
                                SELECT flat_ID, person_ID FROM flat_owner_history_table 
                                WHERE ID in (
                                    SELECT MAX(ID) FROM flat_owner_history_table 
                                    GROUP BY flat_ID  
                                )
                            ) fdd ON fl.flat_ID = fdd.flat_ID 
                            JOIN person p ON fdd.person_ID = p.person_ID 
                        """).fetchall()
    conn.close()
    
    data = [dict(fl) for fl in flats]
    return render_template('flats.html',flats = data)

@app.route('/vehicles')
def vehicles():

    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    vehicles =  conn.execute("""
                                SELECT * FROM vehicle v 
                                JOIN person p ON v.owner_ID =  p.person_ID 
                                JOIN flat f ON p.person_ID = f.occupant_ID
                            """).fetchall()
    conn.close()
    
    data = [dict(vh) for vh in vehicles]
    print("Vehicles")
    print(data)
    return render_template('vehicles.html', vehicles = data)   

@app.route('/settings')
def settings():

    # conn = get_db_connection()
    # conn.row_factory = sqlite3.Row
    # locations = conn.execute('SELECT * FROM location l LEFT JOIN  history h ON h.id = ( SELECT id FROM history WHERE loc_id = l.id ORDER BY date DESC LIMIT 1) ').fetchall()
    # conn.close()
    
    # data = [dict(lc) for lc in locations]
    return render_template('settings.html')  

@app.route('/newvisitor')
def newvisitor():

  
    return render_template('new-visitor.html')  



@app.route('/newvisitor', methods = ['POST'])
def createnewvisitor():
    print( request.form)

   

    visitor_id = request.form['visitor_id']

    visting_flat_id = request.form['visting_flat_id']
    visitor_vehicle = request.form['visitor_vehicle']
    visting_count = request.form['visting_count']
    visitee_id = request.form['visting_member_id']
     
    if( len(visitor_id) == 0):
        conn = get_db_connection()
        cursor = conn.cursor()
        rec = cursor.execute("INSERT INTO person (name, phone_number) VALUES (?,?)",
                            [request.form['person_name'], request.form['person_phone']]
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
        print([visitor_id, visting_flat_id, visitee_id, entry, visitor_vehicle , visting_count])
        newvisitor = cursor.execute("""
                                        INSERT INTO visitor_entry 
                                            (visitor_ID, flat_ID,visitee_ID, entry_time,vehicle_number,no_of_people) 
                                        VALUES (?,?,?,?,?,?)""",
                                    [visitor_id, visting_flat_id, visitee_id, entry, visitor_vehicle , visting_count]
                                    )
    except sqlite3.IntegrityError:
        error='Record already exists in database!'
        return render_template('new-flat.html', error=error)

    person_id = newvisitor.lastrowid;
    print( newvisitor.lastrowid)
    rec2 = conn.commit()

    return redirect('/visitors')


@app.route('/checkoutvisitor' , methods = ['POST'])
def checkoutvisitor():
   

    entry_ID = request.form['entry_ID']
    exit = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
     
    print( type( entry_ID));
    id = int( entry_ID);
    print(   id )
    conn = get_db_connection()
    cursor = conn.cursor()
   
 
    cursor.execute("UPDATE visitor_entry SET exit_time = ? WHERE entry_ID = ?",
                [exit, id])
    rec2 = conn.commit()
    return redirect('/visitors')

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
    
    print(  request.form);
    person_id = request.form['owner_id']
    purchase_date = request.form['purchase']
    isoccupant = 'owneroccupant' in request.form 

    print( 'person_id is ' + person_id)
    if( len(person_id) == 0):
        conn = get_db_connection()

        cursor = conn.cursor()
        rec = cursor.execute("INSERT INTO person (name, phone_number) VALUES (?,?)",
                    [request.form['owner_name'], request.form['owner_phone']]
                    )
    
        person_id = rec.lastrowid;
        print(  rec.lastrowid)
        rec2 = conn.commit()
        print( rec2)
        conn.close()

    conn = get_db_connection()
    cursor = conn.cursor()
    error = ''
    try:
        # if current owner is occupant, update same
        if isoccupant:
            newFlat = cursor.execute("""
                                        INSERT INTO flat 
                                            (flat_no, bldg_no, floor_no,area, occupant_ID) 
                                        VALUES (?,?,?,?,?)""",
                        [request.form['flat_no'], request.form['building_no'], request.form['floor'],request.form['area'],person_id ]
                        )
        else :
            newFlat = cursor.execute("""
                                        INSERT INTO flat 
                                            (flat_no, bldg_no, floor_no,area) 
                                        VALUES (?,?,?,?)""",
                        [request.form['flat_no'], request.form['building_no'], request.form['floor'],request.form['area'] ]
                        )
        
    except sqlite3.IntegrityError:
        error='Record already exists in database!'
        return render_template('new-flat.html', error=error)

    
    print( newFlat.lastrowid)
    rec2 = conn.commit()

    conn = get_db_connection()
    cursor = conn.cursor()
     
     
    newownertxn = cursor.execute("INSERT INTO flat_owner_history_table (flat_ID, person_ID , purchase_date) VALUES (?,? ,?)",
                [newFlat.lastrowid, person_id, purchase_date]
                )
    
    new_owner_txnid = newownertxn.lastrowid
    rec2 = conn.commit()

    if isoccupant:
        conn = get_db_connection()
        cursor = conn.cursor()
        error = ''
         
        cursor.execute("INSERT INTO flat_occupant_history_table (flat_ID, person_ID, type ) VALUES (?,?,?)",
                    [newFlat.lastrowid, person_id, 1]
                    )
        
        rec2 = conn.commit()

    if 'file' in request.files:
        f = request.files['file']
        path = 'static/files/'+ str(new_owner_txnid)
        os.makedirs(path)
        filesaved = os.path.join( path,secure_filename(f.filename))
        f.save(filesaved)
        conn = get_db_connection()
        cursor = conn.cursor()
         
        newocc = cursor.execute("INSERT INTO flat_owner_file_record_table (history_ID, filepath) VALUES(?,?)",
                    [new_owner_txnid , secure_filename(f.filename) ]
                    )
        
        rec2 = conn.commit()
        conn.close()

    return redirect('/flats')

@app.route('/flatedit')
def edit():
    print(request.args)
    flatid = request.args['flatid']

    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    flats = conn.execute("""
                            SELECT * FROM flat fl 
                            JOIN flat_owner_history_table fo ON fl.flat_ID = fo.flat_ID
                            JOIN person p ON fo.person_ID = p.person_ID
                            WHERE p.person_ID in (
                                SELECT person_ID FROM flat_owner_history_table 
                                WHERE flat_ID= ? order by ID DESC LIMIT 1
                            )""",[flatid]
                        ).fetchall()
    conn.close()
    
    data = [dict(fl) for fl in flats]
    print( data);
    return render_template('flatedit.html',flat = data[0])


@app.route('/newflatowner')
def newflatownerrecord():
    flatid = request.args['flatid']

    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    flats = conn.execute("""
                            SELECT * FROM flat fl 
                            JOIN flat_owner_history_table fo ON fl.flat_ID = fo.flat_ID
                            JOIN person p ON fo.person_ID = p.person_ID
                            WHERE p.person_ID in (
                                SELECT person_ID FROM flat_owner_history_table
                                WHERE flat_ID=? order by ID DESC LIMIT 1
                            )""",[flatid]
                        ).fetchall()
    conn.close()
    
    data = [dict(fl) for fl in flats]
    
    return render_template('newflatowner.html', flat = data[0])

@app.route('/newflatowner', methods = ['POST'])
def cratenewflatownerrecord():
    print( request.form)
    new_owner_id  = request.form['new_owner_id']
    flat_ID = request.form['flat_ID']
    curr_owner_id = request.form['owner_id']
    print(request.files['file']);
   
    isoccupant = 'owneroccupant' in request.form 
    print(isoccupant)
    print( 'new_owner_id is ' + new_owner_id)
    if( len(new_owner_id) == 0):
        conn = get_db_connection()

        cursor = conn.cursor()
        rec = cursor.execute("INSERT INTO person (name, phone_number) VALUES (?,?)",
                                [request.form['new_owner_name'], request.form['new_owner_phone']]
                            )
    
        new_owner_id = rec.lastrowid;
        print(  rec.lastrowid)
        rec2 = conn.commit()
        print( rec2)
        conn.close()

    conn = get_db_connection()
    cursor = conn.cursor()
     
    cursor.execute(" UPDATE flat_owner_history_table set sale_date=? WHERE flat_ID = ? AND person_ID = ?",
                    [request.form['saledate'],flat_ID, curr_owner_id ])

    newownertxn = cursor.execute("INSERT INTO flat_owner_history_table (flat_ID, person_ID, purchase_date ) VALUES (?,?,?)",
                [flat_ID, new_owner_id, request.form['saledate']]
                )
    new_owner_txnid = newownertxn.lastrowid  
    rec2 = conn.commit()
    conn.close()

  

    if isoccupant:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        
        cursor.execute("INSERT INTO flat_occupant_history_table (flat_ID, person_ID, type ) VALUES (?,?,? )",
                                    [flat_ID, new_owner_id, 1]
                                )
        
        rec2 = conn.commit()
        conn.close()
        conn = get_db_connection()
        cursor = conn.cursor()
         
        cursor.execute("UPDATE flat set occupant_ID= ? WHERE flat_ID = ?",
                                [new_owner_id , flat_ID ]
                                )
        
        rec2 = conn.commit()
        conn.close()
    
    if 'file' in request.files:
        f = request.files['file']
        path = 'static/files/'+ str(new_owner_txnid)
        os.makedirs(path)
        filesaved = os.path.join( path,secure_filename(f.filename))
        f.save(filesaved)
        conn = get_db_connection()
        cursor = conn.cursor()
         
        newocc = cursor.execute("INSERT INTO flat_owner_file_record_table (history_ID, filepath) VALUES(?,?)",
                    [new_owner_txnid , secure_filename(f.filename) ]
                    )
        
        rec2 = conn.commit()
        conn.close()

    return redirect('/flatdetails?flatid='+flat_ID)

@app.route('/newflattenant')
def newtenantrecord():
    flatid = request.args['flatid']

    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    flats = conn.execute("""
                            SELECT * FROM flat fl 
                            JOIN flat_owner_history_table fo ON fl.flat_ID = fo.flat_ID
                            JOIN person p ON fo.person_ID = p.person_ID
                            WHERE p.person_ID in (
                                SELECT person_ID FROM flat_owner_history_table
                                WHERE flat_ID = ? order by ID DESC LIMIT 1
                            )""",[flatid]
                        ).fetchall()
    conn.close()
    
    data = [dict(fl) for fl in flats]
    
    return render_template('newflattenant.html', flat = data[0])
    
@app.route('/newflattenant', methods = ['POST'])
def cratenewtenantrecord():
    new_tenant_id  = request.form['new_tenant_id']
    flat_ID = request.form['flat_ID']
    startDate = request.form['startdate']
     

    print( 'new_tenant_id is ' + new_tenant_id)
    if( len(new_tenant_id) == 0):
        conn = get_db_connection()

        cursor = conn.cursor()
        rec = cursor.execute("INSERT INTO person (name, phone_number) VALUES (?,?)",
                    [request.form['new_tenant_name'], request.form['new_tenant_phone']]
                    )
    
        new_owner_id = rec.lastrowid;
        print(  rec.lastrowid)
        rec2 = conn.commit()
        print( rec2)
        conn.close()

   
 
    conn = get_db_connection()
    cursor = conn.cursor()
        
    newocc = cursor.execute("INSERT INTO flat_occupant_history_table (flat_ID, person_ID, type , from_date) VALUES (?,?,?,? )",
                [flat_ID, new_owner_id, 2, startDate]
                )
    
    rec2 = conn.commit()
    conn.close()

    conn = get_db_connection()
    cursor = conn.cursor()
        
    cursor.execute("UPDATE flat set occupant_ID= ? WHERE flat_ID = ?",
                [new_owner_id , flat_ID ]
                )
    
    rec2 = conn.commit()
    conn.close()
    
    return redirect('/flatdetails?flatid='+flat_ID)

@app.route('/flatdetails')
def flatdetails():
    flatid = request.args['flatid']

    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    flats = conn.execute("""
                            SELECT * FROM flat fl 
                            JOIN flat_owner_history_table fo ON fl.flat_ID = fo.flat_ID
                            JOIN person p ON fo.person_ID = p.person_ID
                            WHERE p.person_ID in (
                                SELECT person_ID FROM flat_owner_history_table 
                                WHERE flat_ID= ? order by ID DESC LIMIT 1
                            )""",[flatid]
                        ).fetchall()    
    conn.close()
    
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    ownerList = conn.execute("""
                                SELECT * FROM flat fl 
                                JOIN flat_owner_history_table fo ON fl.flat_ID = fo.flat_ID
				JOIN flat_owner_file_record_table ft ON ft.history_ID = fo.ID
                                JOIN person p ON p.person_ID=fo.person_ID
                                WHERE fl.flat_ID=  ?""",[flatid]
                            ).fetchall()
    conn.close()
    
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    tenantList = conn.execute("""
                                SELECT * FROM flat fl 
                                JOIN flat_occupant_history_table fo ON fl.flat_ID = fo.flat_ID
                                JOIN person p ON p.person_ID=fo.person_ID
                                WHERE fl.flat_ID=? AND fo.type = 2""",[flatid]
                            ).fetchall()
    conn.close()
    

    data = [dict(fl) for fl in flats]
    
    return render_template('flatdetails.html', flat = data[0], ownerList=ownerList, tenantList=tenantList)

@app.route('/newvehicle')
def newvehicle():
    return render_template('new-vehicle.html')  


@app.route('/newvehicle', methods = ['POST'])
def createnewvehicle():
    print(  request.form);
    person_id = request.form['owner_ID']
    print( 'person_id is ' + person_id)
   
    conn = get_db_connection()
    cursor = conn.cursor()
    error = ''
    try:
        newVehicle = cursor.execute("INSERT INTO vehicle (vehicle_ID, make, model, owner_ID, type) VALUES (?,?,?,?,?)",
                    [request.form['vehicle_number'],request.form['make'], request.form['model'], person_id,request.form['type'] ]
                    )
    except sqlite3.IntegrityError:
        error='Record already exists in database!'
        return render_template('new-vehicle.html', error=error)

    person_id = newVehicle.lastrowid;
    print( newVehicle.lastrowid)
    rec2 = conn.commit()
    return redirect('/vehicles') 



@app.route('/person/owner' )
def getownerlist():

    name = request.args['query']
    name = '%'+name+'%'
    print( name)
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    owners = conn.execute("""
                            SELECT * FROM person p 
                            JOIN flat_occupant_history_table of ON p.person_ID = of.person_ID
                            JOIN flat f ON f.flat_ID = of.flat_ID
                            WHERE p.name like ? """,[name]
                        ).fetchall()
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
    owners = conn.execute("""
                            SELECT * FROM person p 
                            WHERE p.phone_number like ? """,[phno]
                        ).fetchall()
    conn.close()

    data = [dict(lc) for lc in owners]
    print (data)

    return data



if __name__ == '__main__':
    app.run(debug=True)

