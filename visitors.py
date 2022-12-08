import sqlite3
import json
import os
from tkinter import E
from flask import Flask, render_template, request, redirect, jsonify
from datetime import datetime


def get_db_connection():
    conn = sqlite3.connect('isoc.db')
    conn.row_factory = sqlite3.Row
    return conn

def getVisitors( qry):

    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    query = """
            SELECT p.name AS vname, v.entry_ID, v.visitor_ID, v.vehicle_number, p.phone_number AS vph,
                v.no_of_people, v.entry_time, v.exit_time, f.flat_no, f.bldg_no, po.name 
            FROM visitor_entry v
            JOIN person p ON v.visitor_ID = p.person_ID
            JOIN flat f on v.flat_ID = f.flat_ID
            JOIN person po ON v.visitee_ID=po.person_ID """

    if( qry == '1'):
        query = query + " WHERE exit_time IS NULL"
    query = query + ";"
    visitors = conn.execute(query).fetchall()
    conn.close()
    print("Visitors query:\n", visitors)
    return visitors