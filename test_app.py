# from flask_sqlalchemy import SQLAlchemy
from models import User, Products
from flask import Response
from werkzeug.http import parse_cookie
from jwt import decode


class TestSpeedyMartApp:
    def test_example(self, app_obj, db_obj):
        app = app_obj
        with app.app_context():
            users_count = User.query.count()
            assert users_count == 1
            products_count = Products.query.count()
            assert products_count == 5

    def test_account_register(self, app_obj, test_client, db_obj):
        app = app_obj
        account_data = {
            "name": "Gokul",
            "email": "gcy@gmail.com",
            "password": "1234",
        }
        # hashed_password = generate_password_hash("1234", "scrypt")
        with app.app_context():
            response: Response = test_client.post("/register", data=account_data)
            # print(response.data)
            assert response.status_code == 302
            # print(Account.query.all())
            acc = User.query.filter(User.email == "gcy@gmail.com").all()
            # print(acc)
            assert len(acc) == 1
            assert acc[0].name == "Gokul"
            # print(acc[0].to_dict())

    def test_account_login(self, app_obj, test_client, db_obj):
        app = app_obj
        acc_login = {
            "email": "g@g.com",
            "password": "1234",
        }
        with app.app_context():
            response: Response = test_client.post("/login", data=acc_login)
            assert response.status_code == 302
            cookies = response.headers.getlist("Set-Cookie")
            cookie_attrs = parse_cookie(cookies[0])
            print(cookie_attrs)
            access_token_cookie = cookie_attrs["access_token_cookie"]
            decoded_jwt = decode(
                access_token_cookie, "jwt-secret-string-!@#", ["HS256"]
            )
            # print(decoded_jwt)
            assert decoded_jwt["email"] == "g@g.com"
