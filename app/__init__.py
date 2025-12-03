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


def standardize():
    