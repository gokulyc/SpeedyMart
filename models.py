from flask_sqlalchemy import SQLAlchemy
# import sqlalchemy as sa
# from datetime import datetime, UTC

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    # username = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200))

    def to_dict(self, exclude_password=True):
        di = {
            "id": self.id,
            "email": self.email,
            "name": self.name,
        }
        if exclude_password:
            return di
        else:
            return {**di, **{"password": self.password}}


class Products(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)

    def to_dict(self):
        di = {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "image_url": self.image_url,
        }
        return di.copy()
