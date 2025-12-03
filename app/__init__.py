#GLOBALS

#import
from flask import Flask, render_template, request, session, url_for, redirect
import sqlite3

#db cursor
DB_FILE = "__FILENAME__.db"
db = sqlite3.connect(DB_FILE)
cursor = db.cursor()

#


#--------------------------------------------------------------------------
#CODE

#QoL db commands
def accessitem(tablename, columnname): #accesses "columnname" from a chosen "tablename" in db
    cursor.execute(f"Select"+columnname+"from"+tablename)

def accessitem_s(tablename, columnname, itemname): #accesses a single item from a given column
    