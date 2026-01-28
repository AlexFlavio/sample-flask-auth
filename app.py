from flask import Flask, jsonify,request
from models.user import User
from database import db
from flask_login import LoginManager, login_user,current_user,logout_user,login_required


app:Flask = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

login_manager = LoginManager()

db.init_app(app)
login_manager.init_app(app)

login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route("/login",methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            print(current_user.is_authenticated)

            return jsonify({"message": "authenticated"})
    
    return jsonify({"message": "invalid credentials!"}),400


@app.route("/logout",methods=["GET"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"})


@app.route("/user",methods=["POST"])
def create_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    if username and password:
        user = User(username=username,password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User has been registered successfully"})
    return jsonify({"message":"invalid credentials!"}),401
    ...

@app.route("/user/<id_user>",methods=["GET"])
@login_required
def read_user(id_user):
    user = User.query.get(id_user)

    if user:
        return jsonify({"username": user.username})
    
    return jsonify({"message":"user not found"}),404

@app.route("/user/<id_user>",methods=["PUT"])
@login_required
def update_user(id_user):
    data = request.json
    user = User.query.get(id_user)

    if user and data.get("password"):
        if current_user.id != user.id:
            return jsonify({"message": "You can only change your own password."}), 400
        
        user.password = data.get("password")
        db.session.commit()
        
        return jsonify({"message": f"user {id_user} updated successfully"})

    return jsonify({"message":"user not found"}),404



@app.route("/user/<id_user>",methods=["DELETE"])
@login_required
def delete_user(id_user):
    data = request.json
    user = User.query.get(id_user)

    if id_user == current_user.id:
        return jsonify({"message": "Deletion not allowed"}), 403

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"user {id_user} deleted successfully"})

    return jsonify({"message":"user not found"}),404


if __name__ == "__main__":
    app.run(debug=True)