from . import db

class User(db.Model):
    __tableName__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(100), nullable=False)
    lastName = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), unique=True, nullable=False)
    created_at= db.Column(db.DateTime(timezone=True), server_Default=func.now())

    def __repr__(self):
        return f'<User {self.firstName} {self.id}'