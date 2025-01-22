from . import app
from .. import db
from flask import request, make_response
from app.models import Users, Funds
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from functools import wraps
from sqlalchemy.sql import func


@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    firstName = data.get("firstName")
    lastName = data.get("lastName")
    email = data.get("email")
    password = data.get("password")

    if firstName and lastName and email and password:
        user = Users.query.filter_by(email=email).first()
        if user:
            return make_response({"message": "Please Sign in"}, 200)
        user = Users(
            email=email,
            password=generate_password_hash(password),
            firstName=firstName,
            lastName=lastName,
        )
        db.session.add(user)
        db.session.commit()
        return make_response(
            {"message": "User Created"},
            201,
        )
    return make_response({"message": "Unable to create user"}, 500)


@app.route("/login", methods=["POST"])
def login():
    auth = request.json
    if not auth or not auth.get("email") or not auth.get("password"):
        return make_response({"message": "Proper credentials were not provided"}, 401)
    user = Users.query.filter_by(email=auth.get("email")).first()
    if not user:
        return make_response(
            "Please create an account",
            401,
        )
    if check_password_hash(user.password, auth.get("password")):
        token = jwt.encode(
            {
                "id": user.id,
                "exp": datetime.utcnow() + timedelta(minutes=30),
            },
            "secret",
            "HS256",
        )
        return make_response({"token": token}, 201)
    return make_response(
        "Please check your credentials",
        401,
    )


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
        if not token:
            return make_response({"Message": "Token is missing"}, 401)
        try:
            data = jwt.decode(token, "secret", algorithms=["HS256"])
            current_user = Users.query.filter_by(id=data["id"]).first()
        except Exception as e:
            print(e)
            return make_response({"Message": "Token is invalid"}, 401)
        return f(current_user, *args, **kwargs)

    return decorated


@app.routes("/funds", methods=["GET"])
@token_required
def getAllFunds(current_user):
    funds = Funds.query.filter_by(userId=current_user.id).all()
    totalSum = 0
    if funds:
        totalSum = (
            Funds.query.with_entities(db.func.round(func.sum(Funds.amount), 2))
            .filter_by(userId=current_user.id)
            .all()
        )[0][0]
    return make_response(
        {
            "data": [fund.serialize for fund in funds],
            "sum": totalSum,
        }
    )
