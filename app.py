from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("DB_URL") or "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users" 

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)

    def json(self):
        return {"id": self.id, "username": self.username, "email": self.email}



with app.app_context():
    db.create_all()

#test route usiing CRUD pattern
@app.route("/test", methods=["GET"])
def test():
    return make_response(jsonify({"message": "API is working!"}), 200)


# user routes
@app.route("/users", methods=["POST"])
def create_user():
    try:
        data = request.get_json() or {}
        if "username" not in data or "email" not in data:
            return make_response(jsonify({"error": "username and email are required"}), 400)

        new_user = User(username=data["username"], email=data["email"])
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify(new_user.json()), 201)
    except Exception:
        db.session.rollback()
        return make_response(jsonify({"error": "error creating user"}), 500)


@app.route("/users", methods=["GET"])
def get_users():
    try:
        users = User.query.all()
        return make_response(jsonify([user.json() for user in users]), 200)
    except Exception:
        return make_response(jsonify({"error": "error fetching users"}), 500)


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    try:
        user = db.session.get(User, user_id)  # modern SQLAlchemy pattern
        if not user:
            return make_response(jsonify({"error": "User not found"}), 404)
        return make_response(jsonify(user.json()), 200)
    except Exception:
        return make_response(jsonify({"error": "error fetching user"}), 500)


@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        user = db.session.get(User, user_id)
        if not user:
            return make_response(jsonify({"error": "User not found"}), 404)

        db.session.delete(user)
        db.session.commit()
        return make_response(jsonify({"message": "User deleted successfully"}), 200)
    except Exception:
        db.session.rollback()
        return make_response(jsonify({"error": "error deleting user"}), 500)


@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    try:
        user = db.session.get(User, user_id)
        if not user:
            return make_response(jsonify({"error": "User not found"}), 404)

        data = request.get_json() or {}
        if "username" not in data or "email" not in data:
            return make_response(jsonify({"error": "username and email are required"}), 400)

        user.username = data["username"]
        user.email = data["email"]
        db.session.commit()
        return make_response(jsonify({"message": "User updated successfully"}), 200)
    except Exception:
        db.session.rollback()
        return make_response(jsonify({"error": "error updating user"}), 500)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000)