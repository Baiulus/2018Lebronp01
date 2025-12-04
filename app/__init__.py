#GLOBALS

#import
from flask import Flask, render_template, request, session, url_for, redirect
import sqlite3, os

app = Flask(__name__)
app.secret_key = os.urandom(24)

#db cursor
DB_FILE = "__FILENAME__.db"
db = sqlite3.connect(DB_FILE)
cursor = db.cursor()
#

@app.route("/")
def disp_homepage():
    # we dont have a proper session username set up so this is used for testing !! 
    # session['username'] = "bronbron" 
    return render_template("homepage.html")

@app.route("/login", methods = ["GET", "POST"])
def disp_login():
    return render_template("login.html")

@app.route("/createaccount", methods = ["GET", "POST"])
def disp_createaccount():
    return render_template("createaccount.html")


#--------------------------------------------------------------------------
#CODE

#QoL db commands
def accessitem(tablename, columnname): #accesses "columnname" from a chosen "tablename" in db
    cursor.execute(f"Select"+columnname+"from"+tablename) #input: select [__COLUMNNAME__] from [__TABLENAME__]

# def accessitem_s(tablename, columnname, itemname): #accesses a single item from a given column
    # uhhh don't push broken code pls


def accessitem_s(tablename, columnname, itemname): #accesses a single item from a given column
    cursor.execute(f"Select * from"+tablename+"where"+columnname+"= '"+ itemname + "'") #input: select * from [__TABLENAME__] where [__COLUMNNAME__] = '[__ITEMNAME__]'
    
def accessitem_m(tablename, columnname, itemarray): #accesses any item from the itemarray in a given column
    
    for item in itemarray: #adds [']s to each item in itemarray to make it readable by sqlite
        item = "'"+item+"'" 
    
    items = ', '.join(map(str, itemarray)) #removes the brackets from itemarray to make items readable by sqlite
    
    cursor.execute(f"Select * from" + tablename + "where" + columnname + "in (" + items + ")") #input: select * from [__TABLENAME__] where [__COLUMNNAME__] in [__ITEMS__]
    
    
#--------------------------------------------------------------------------
#TESTS


if __name__ == "__main__":
    app.debug = True
    app.run()
