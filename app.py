from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["ecommerce_db"]
users = db["users"]
orders = db["orders"]
# ---------------- ROUTES ---------------- #
@app.route("/")
def home():
    return render_template("task1.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/signup")
def signup_page():
    return render_template("signup.html")

@app.route("/addtocart")
def cart_page():
    return render_template("addtocart.html")
@app.route("/profile")
def profile():
    return render_template("profile.html")
@app.route("/shop")
def shop():
    return render_template("shop.html")
@app.route("/women")
def women():
    return render_template("women.html")
@app.route("/men")
def men():
    return render_template("men.html")
@app.route("/accessories")
def accessories():
    return render_template("accessories.html")
@app.route("/blog")
def blog():
    return render_template("blog.html")
@app.route("/payment_success")
def payment_success():
    return render_template("payment_success.html")
# ---------------- AUTH ---------------- #
@app.route("/templates/signup", methods=["POST"])
def signup():
    data = request.json
    if users.find_one({"email": data["email"]}):
        return jsonify({"msg": "User already exists"}), 400
    users.insert_one({
        "name": data.get("name"),
        "email": data.get("email"),
        "password": data.get("password")
    })
    return jsonify({"msg": "Signup successful"})
@app.route("/templates/login", methods=["POST"])
def login():
    data = request.get_json()
    email=data.get("email")
    password=data.get("password")
    user = users.find_one({
        "email": data["email"],
        "password": data["password"]
    })
    if user:
      return jsonify({
        "msg":"Login success",
        "name":user.get("name","User"),
        "email":user.get("email")
      }),200
    else:
        return jsonify({"msg":"Invalid credentials"}),401
# ---------------- CART / ORDER ---------------- #
@app.route("/addtocart", methods=["POST"])
def place_order():
    data = request.json
    orders.insert_one({
        "user": data["email"],
        "items": data["cart"],
        "total": data["total"]
    })
    return jsonify({"msg": "Order placed successfully"})
# ---------------- RUN ---------------- #
if __name__ == "__main__":
    app.run(debug=True)