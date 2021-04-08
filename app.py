from flask import Flask, request, render_template, redirect, session, url_for, jsonify
import mysql.connector

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="mydog8229",
    database="mydatabase"
)

mycursor = mydb.cursor(buffered=True)





app=Flask(__name__, static_folder="static", static_url_path="/static")
app.secret_key ="abc"


@app.route("/")
def index():
    return render_template("loginpage.html")
    

@app.route("/api/users", methods=["GET"])
def data_all():
    sql_username=request.args["username"]
    mycursor.execute("SELECT * FROM user WHERE username='%s'" % (sql_username))
    row=mycursor.fetchone()
    print(row)
    if row != None:
        return jsonify({"data":{
        "id": row[0],
        "name": row[1],
        "username": row[2],
        "password": row[3]
    }})

    else:
        data={"data":"null"}
        return jsonify(data)


@app.route("/signin", methods=["POST"])
def signin():
    signin_account=request.form["username"]
    signin_pw=request.form["password"]
    mycursor.execute("SELECT * FROM user WHERE username='%s' and password='%s'" % (signin_account, signin_pw))
    myrecord = mycursor.fetchone()
    print (myrecord)
    # return "ok"
    if myrecord != None:
        session["id_name"]= myrecord[1]
        session["account"]=myrecord[2]
        return redirect(url_for("member"))
    else:
        return redirect("/error?message=帳號或密碼輸入錯誤")

@app.route("/signup", methods=["POST"])
def signup():
    id_name=request.form["name"]
    signup_account=request.form["username"]
    signup_pw=request.form["password"]
    mycursor.execute("SELECT * FROM user WHERE username='%s'" % (signup_account))
    myresult = mycursor.fetchone()
    print (myresult)
    # return "ok"
    if myresult != None:      
        return redirect("/error?message=帳號已經被註冊")
    else:
        session["id_name"]=request.form["name"]
        mycursor.execute("INSERT INTO user (name, username, password) VALUES (%s, %s, %s)",(id_name, signup_account, signup_pw))
        mydb.commit()
        return redirect("/")



@app.route("/member")
def member():

    if "account" in session:
        return render_template("member.html")
    else:
        return redirect("/")


@app.route("/error")
def error():
    comment=request.args.get("message")
    print (comment)
    return render_template("error.html", message=comment)

@app.route("/signout")
def signout():
    session.pop("account", None)
    return redirect("/")



app.run(port=3000)

