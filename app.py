from . import app, db
from flask import request, make_response
from .models import Users, Funds
from werkzeug.security import generate_password_hash, check_password_hash


@app.route("/signup", ["POST"])
def signup():
    data = request.json
    email = data.get("email")
    firstName = data.get("firstName")
    lastName = data.get("lastName")
    password = data.get("password")

    if firstName and lastName and email and password:
        user = Users.query.filter_by(email=email).first()
        if user:
            return make_response({"message": "Please Sign in"}, 200)
        user = Users(
            email=email,
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
