from flask import render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import NotFound
from flask_jwt_extended import (
    JWTManager,
    current_user,
    jwt_required,
    create_access_token,
    set_access_cookies,
    unset_jwt_cookies,
)

from models import db, Products, User
from forms import RegisterForm, AddProductForm
from sample_data import products_sample
from flask_app_db_factory import get_flask_env_app
import os

app = get_flask_env_app()

app.config["JWT_SECRET_KEY"] = (
    "jwt-secret-string-!@#"  # Use a real secret key in production
)
app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies", "json", "query_string"]

jwt = JWTManager(app)


@jwt.unauthorized_loader
def custom_unauthorized_response(_err):
    return redirect(url_for("login", message="AnonymousUser"))


@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
    return redirect(url_for("login", message="TokenExpired"))


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter(User.email == identity["email"]).one_or_none()


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    # print(form.data)
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method="scrypt")
        new_user = User(
            email=form.email.data,
            name=form.name.data,
            password=hashed_password,
        )
        db.session.add(new_user)
        db.session.commit()
        flash("User registered..., Please login.")
        return redirect(url_for("dashboard"))
    else:
        print(form.errors)
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    message = request.args.get("message")
    if request.method == "POST":
        user: User = User.query.filter_by(email=request.form["email"]).first()
        if user and check_password_hash(user.password, request.form["password"]):
            additional_claims = {**user.to_dict()}
            access_token = create_access_token(
                identity={"email": user.email},
                additional_claims=additional_claims,
            )
            response = redirect("/dashboard")
            set_access_cookies(response, access_token)
            return response
    return render_template("login.html", message=message)


@app.route("/dashboard")
@jwt_required()
def dashboard():
    account: User = User.query.filter(User.email == current_user.email).one().to_dict()
    return render_template("dashboard.html", account=account)


@app.route("/add_product", methods=["GET", "POST"])
def add_product():
    form = AddProductForm()
    # print(form.data)
    if form.validate_on_submit():
        new_product = Products(
            name=form.name.data,
            category=form.category.data,
            image_url=form.image_url.data,
        )
        db.session.add(new_product)
        db.session.commit()
        flash("Product registered")
        return render_template("add_product.html", form=form)
    else:
        print(form.errors)
    return render_template("add_product.html", form=form)


@app.route("/list_products")
def list_products():
    products: list[Products] = [p.to_dict() for p in Products.query.all()]
    # print(products)
    if len(products) == 0:
        raise NotFound
    return render_template("products_all.html", products=products)


@app.route("/logout", methods=["GET"])
def logout_with_cookies():
    response = redirect("/")
    unset_jwt_cookies(response)
    return response


def add_accounts_data():
    try:
        db.session.add(
            User(
                name="Gokul Y",
                email="g@g.com",
                password=generate_password_hash("1234", method="scrypt"),
            )
        )
        db.session.commit()
        print("User g@g.com added!")
    except Exception as e:
        print(f"Unable to add User : {e}")


def add_products_sample_data():
    try:
        for product in products_sample:
            db.session.add(Products(**product))
            db.session.commit()
        print("Sample Products added!")
    except Exception as e:
        print(f"Unable to add products : {e}")


if __name__ == "__main__":
    with app.app_context():
        db.init_app(app)
        try:
            # db.drop_all()
            db.create_all()
            add_accounts_data()
            add_products_sample_data()
        except Exception as e:
            print(e)
    app.run(host=os.getenv("BACKEND_FLASK_HOST", "127.0.0.1"))
