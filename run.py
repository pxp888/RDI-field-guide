import os
import json
from flask import Flask, render_template, request, flash
if os.path.exists("env.py"):
    import env

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
        # print(request.form)
        flash("Thanks {}, we have received your message!".format(
            request.form.get("first_name")))
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        debug=True)

