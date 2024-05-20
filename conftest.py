from models import Products, User

# from flask_app_db_factory import get_test_env_app, db
import pytest
from sample_data import products_sample
from werkzeug.security import generate_password_hash
from main import app, db


def add_accounts_data(db):
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


def add_products_sample_data(db):
    try:
        for product in products_sample:
            db.session.add(Products(**product))
            db.session.commit()
        print("Sample Products added!")
    except Exception as e:
        print(f"Unable to add products : {e}")


@pytest.fixture(scope="class")
def app_obj():
    app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///test.db",
            "WTF_CSRF_ENABLED": False,
        }
    )

    yield app


@pytest.fixture(scope="class")
def db_obj(app_obj):
    db.init_app(app_obj)
    with app_obj.app_context():
        db.create_all()
        try:
            add_accounts_data(db)
            add_products_sample_data(db)
        except Exception as e:
            print(e)
    yield db
    try:
        with app_obj.app_context():
            db.drop_all()
    except Exception as e:
        print(e)
        print("unable to drop tables.")


@pytest.fixture
def test_client(app_obj):
    app = app_obj
    return app.test_client()
