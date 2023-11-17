import os
import json
import time
from flask import Flask, render_template, request, flash
import psycopg2
import requests

if os.path.exists("env.py"):
    import env


db_connection = None


def getDBConnection():
    # This is a helper function used by the database calls below to get
    # a database connection.
    # This enables the same connection to be used for multiple calls,
    # and re-establishes the connection if it is lost.
    # The database connection details are stored in environment variables.

    db_pw = os.environ.get('DB_PW')
    db_ip = os.environ.get('DB_IP')
    if db_ip is None:
        db_ip = "localhost"

    global db_connection
    if db_connection is None or db_connection.closed != 0:
        try:
            db_connection = psycopg2.connect(
                host=db_ip,
                database="postgres",
                user="postgres",
                password=db_pw
            )
        except psycopg2.OperationalError:
            # if the connection times out, re-establish it
            db_connection = psycopg2.connect(
                host=db_ip,
                database="postgres",
                user="postgres",
                password=db_pw
            )
    return db_connection


def setupStorage():
    # create database tables if they don't exist.  This should only
    # be called once at the start of the application.
    conn = getDBConnection()
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS contacts
        (ID SERIAL PRIMARY KEY,
        PTIME TEXT,
        FNAME TEXT,
        LNAME TEXT,
        EMAIL TEXT,
        COMPANY TEXT,
        MSG TEXT);''')
    conn.commit()
    cur.close()


def saveMessage(data):
    conn = getDBConnection()
    cur = conn.cursor()
    cur.execute("INSERT INTO contacts (PTIME, FNAME, LNAME, EMAIL, COMPANY, MSG) VALUES (%s, %s, %s, %s, %s, %s)", data)
    conn.commit()
    cur.close()


def ntfy(data):
    msg = str(data)
    requests.post("http://52.56.34.125/rdi", data=msg.encode(encoding='utf-8'))


def gotmsg(msg):
    data = (str(time.asctime()), msg["first_name"], msg["last_name"], msg["email"], msg["company-name"], msg["message"])
    saveMessage(data)
    ntfy(data)
    # print(data)


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/introduction")
def introduction():
    return render_template("introduction.html")


@app.route("/marketing")
def marketing():
    return render_template("marketing.html")


@app.route("/branding")
def branding():
    return render_template("branding.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        flash("Thanks {}, we have received your message!".format(
            request.form.get("first_name")))
        gotmsg(request.form)
    return render_template("contact.html")


if __name__ == "__main__":
    setupStorage()

    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        debug=True)

