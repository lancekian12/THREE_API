from .. import db
from sqlalchemy.sql import func


class Users(db.Model):
    __tablename__ = "users"  # Use lowercase for consistency
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(100), nullable=False)
    lastName = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    funds = db.relationship("Funds", backref="user", cascade="all, delete")

    def __repr__(self):
        return f"<User {self.firstName}>"


class Funds(db.Model):
    __tablename__ = "funds"  # Use lowercase for consistency
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    userId = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )  # Ensure 'users.id' matches the __tablename__ in Users
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            "id": self.id,
            "amount": self.amount,
            "created_at": self.created_at,
        }
