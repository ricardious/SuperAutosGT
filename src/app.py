from flask import Flask, render_template, request, redirect, url_for, flash

from config import config

from models.ModelUser import ModelUser

from models.entities.User import User

from flask_login import LoginManager, login_user, login_required, logout_user

from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
csrf = CSRFProtect()
login_manager_app = LoginManager(app)

# Temporal storage for cars
car_inventory = []


@login_manager_app.user_loader
def load_user(username):
    return ModelUser.get_user(username)


@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = ModelUser.get_user(username)
        if user and user.password == password:
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid username or password"
            return render_template("auth/login.html", error=error)
    return render_template("auth/login.html")


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("auth/dashboard.html")


@app.route("/add-car", methods=["GET", "POST"])
@login_required
def add_car():
    if request.method == "POST":
        car_type = request.form["carType"]
        brand = request.form["brand"]
        model = request.form["model"]
        price = request.form["price"]
        quantity = request.form["quantity"]
        description = request.form["description"]
        image = request.form["image"]

        # Check if car type already exists
        if any(car["car_type"] == car_type for car in car_inventory):
            flash(
                "Car Type ID already exists. Please delete it first if you want to re-register."
            )
        else:
            new_car = {
                "car_type": car_type,
                "brand": brand,
                "model": model,
                "price": price,
                "quantity": quantity,
                "description": description,
                "image": image,
            }
            car_inventory.append(new_car)
            flash("Car registered successfully!")

        return redirect(url_for("cars"))

    return render_template("dashboard/add-car.html")


@app.route("/cars", methods=["GET", "POST"])
@login_required
def cars():
    return render_template("auth/cars.html", cars=car_inventory)


@app.route("/delete-car/<car_type>")
@login_required
def delete_car(car_type):
    global car_inventory
    car_inventory = [car for car in car_inventory if car["car_type"] != car_type]
    flash("Car deleted successfully!")
    return redirect(url_for("cars"))


def status_401(error):
    return redirect(url_for("login"))


def status_404(error):
    return "Page not found"


if __name__ == "__main__":
    app.config.from_object(config["development"])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()
