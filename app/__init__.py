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
    cursor.execute(f"Select"+columnname+"from"+tablename) #input: select [__COLUMNNAME__] from [__TABLENAME__]

def accessitem_s(tablename, columnname, itemname): #accesses a single item from a given column
    cursor.execute(f"Select * from"+tablename+"where"+columnname+"= '"+ itemname + "'") #input: select * from [__TABLENAME__] where [__COLUMNNAME__] = '[__ITEMNAME__]'
    
def accessitem_m(tablename, columnname, itemarray): #accesses any item from the itemarray in a given column
    
    for item in itemarray: #adds [']s to each item in itemarray to make it readable by sqlite
        item = "'"+item+"'" 
    
    items = ', '.join(map(str, itemarray)) #removes the brackets from itemarray to make items readable by sqlite
    
    cursor.execute(f"Select * from" + tablename + "where" + columnname + "in (" + items + ")") #input: select * from [__TABLENAME__] where [__COLUMNNAME__] in [__ITEMS__]
    
    
#--------------------------------------------------------------------------
#TESTS

