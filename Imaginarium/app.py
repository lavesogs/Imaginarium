import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify, send_from_directory
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, apology
from werkzeug.utils import secure_filename

# Initialize the Flask application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['UPLOAD_FOLDER'] = 'uploads/'  # Your uploads folder
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    user_id = session["user_id"]
    user = db.execute("SELECT * FROM users WHERE id = ?", user_id)[0]
    images = db.execute("SELECT * FROM images WHERE user_id = ?", user_id)
    return render_template("index.html", user=user, images=images)

@app.route("/home")
@login_required
def home():
    user_id = session["user_id"]
    user = db.execute("SELECT * FROM users WHERE id = ?", user_id)[0]  # Fetch user data
    images = db.execute("SELECT * FROM images WHERE user_id = ?", user_id)
    return render_template("index.html", user=user, images=images)

@app.route("/profile")
@login_required
def profile():
    user_id = session["user_id"]
    user = db.execute("SELECT * FROM users WHERE id = ?", user_id)[0]
    return render_template("profile.html", user=user)

@app.route("/update_profile", methods=["POST"])
@login_required
def update_profile():
    user_id = session["user_id"]
    username = request.form.get("username")
    email = request.form.get("email")
    bio = request.form.get("bio")
    facebook_url = request.form.get("facebook_url")
    instagram_url = request.form.get("instagram_url")

    if not username or not email:
        return apology("must provide username and email", 400)

    db.execute("UPDATE users SET username = ?, email = ?, bio = ?, facebook_url = ?, instagram_url = ? WHERE id = ?", username, email, bio, facebook_url, instagram_url, user_id)
    flash("Profile updated!")
    return redirect("/profile")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return apology("must provide username and password", 403)

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) != 1 or not check_password_hash(rows[0]["password_hash"], password):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]
        return redirect("/")
    return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")

    if not username or not email or not password or not confirmation:
        return apology("must fill out all fields")
    if password != confirmation:
        return apology("passwords do not match")

    password_hash = generate_password_hash(password)
    try:
        new_user_id = db.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)", username, email, password_hash)
        session["user_id"] = new_user_id
        return redirect("/")
    except Exception:
        return apology("username or email already exists")

@app.route("/upload")
@login_required
def upload():
    # Fetch user images
    user_images = db.execute("SELECT * FROM images WHERE user_id = ?", session["user_id"])
    return render_template("upload.html", user_images=user_images)

@app.route("/upload_image", methods=["GET", "POST"])
@login_required
def upload_image():
    if request.method == "POST":
        if 'image_file' not in request.files:
            return apology("no file part")
        file = request.files['image_file']
        if file.filename == '':
            return apology("no selected file")

        image_name = request.form.get("image_name")
        if not image_name:
            return apology("Image name is required")

        # Check if an image with the same name already exists
        existing_image = db.execute("SELECT * FROM images WHERE user_id = ? AND image_name = ?", session["user_id"], image_name)
        if existing_image:
            flash("An image with that name already exists. Please choose a different name.")
            return redirect("/upload_image")

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # Ensure the upload folder exists
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])

            file.save(file_path)
            db.execute("INSERT INTO images (user_id, image_url, image_name) VALUES (?, ?, ?)", session["user_id"], filename, image_name)
            flash("Image uploaded!")
            return redirect("/upload_image")

    # Fetch user images
    user_images = db.execute("SELECT * FROM images WHERE user_id = ?", session["user_id"])
    return render_template("upload.html", user_images=user_images)

@app.route("/delete_image/<int:image_id>", methods=["DELETE"])
@login_required
def delete_image(image_id):
    # Delete image record from the database
    db.execute("DELETE FROM images WHERE id = ? AND user_id = ?", image_id, session["user_id"])
    return '', 200

@app.route("/update_image_name/<int:image_id>", methods=["POST"])
@login_required
def update_image_name(image_id):
    new_image_name = request.form.get("new_image_name")

    # Check if the new name already exists for the same user
    existing_image = db.execute("SELECT * FROM images WHERE user_id = ? AND image_name = ?", session["user_id"], new_image_name)
    if existing_image:
        flash("An image with this name already exists. Please choose a different name.")
        return redirect("/upload")  # Redirect back to the upload page

    # Update the image name
    db.execute("UPDATE images SET image_name = ? WHERE id = ? AND user_id = ?", new_image_name, image_id, session["user_id"])
    flash("Image name updated!")
    return redirect("/upload")  # Redirect back to the upload page

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/like_image/<int:image_id>", methods=["POST"])
@login_required
def like_image(image_id):
    db.execute("INSERT OR IGNORE INTO likes (user_id, image_id) VALUES (?, ?)", session["user_id"], image_id)
    db.execute("UPDATE images SET like_count = (SELECT COUNT(*) FROM likes WHERE image_id = images.id) WHERE id = ?", image_id)
    return '', 200

@app.route("/comment_image/<int:image_id>", methods=["POST"])
@login_required
def comment_image(image_id):
    comment_text = request.json.get("comment_text")
    db.execute("INSERT INTO comments (user_id, image_id, comment_text) VALUES (?, ?, ?)", session["user_id"], image_id, comment_text)
    return '', 200

@app.route("/get_comments/<int:image_id>")
@login_required
def get_comments(image_id):
    comments = db.execute("SELECT comments.*, users.username FROM comments JOIN users ON comments.user_id = users.id WHERE image_id = ?", image_id)
    comments_html = ''
    for comment in comments:
        comments_html += f'<p><strong>{comment["username"]}:</strong> {comment["comment_text"]}</p>'
        if comment["user_id"] == session["user_id"]:
            comments_html += f'<button onclick="editComment({comment["id"]})">Edit</button>'
            comments_html += f'<button onclick="deleteComment({comment["id"]})">Delete</button>'
    return comments_html

@app.route("/edit_comment/<int:comment_id>", methods=["POST"])
@login_required
def edit_comment(comment_id):
    new_text = request.json.get("new_text")
    db.execute("UPDATE comments SET comment_text = ? WHERE id = ? AND user_id = ?", new_text, comment_id, session["user_id"])
    return '', 200

@app.route("/delete_comment/<int:comment_id>", methods=["DELETE"])
@login_required
def delete_comment(comment_id):
    db.execute("DELETE FROM comments WHERE id = ? AND user_id = ?", comment_id, session["user_id"])
    return '', 200

@app.route("/user_gallery/<int:user_id>")
@login_required
def user_gallery(user_id):
    user = db.execute("SELECT * FROM users WHERE id = ?", user_id)[0]
    images = db.execute("SELECT *, (SELECT COUNT(*) FROM likes WHERE image_id = images.id) as like_count FROM images WHERE user_id = ?", user_id)
    return render_template("user_gallery.html", user=user, images=images)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@app.route("/artists")
@login_required
def artists():
    images = db.execute("SELECT images.*, users.username FROM images JOIN users ON images.user_id = users.id")
    return render_template("artists.html", images=images)

@app.route("/explore_artists")
@login_required
def explore_artists():
    images = db.execute("SELECT * FROM images JOIN users ON images.user_id = users.id")
    return render_template("explore_artists.html", images=images)

@app.route("/explore")
@login_required
def explore():
    artists_images = db.execute("SELECT images.*, users.username FROM images JOIN users ON images.user_id = users.id")
    return render_template("explore.html", artists_images=artists_images)

@app.route("/public_profile/<int:user_id>")
def public_profile(user_id):
    user = db.execute("SELECT * FROM users WHERE id = ?", user_id)[0]
    images = db.execute("SELECT * FROM images WHERE user_id = ?", user_id)
    return render_template("public_profile.html", user=user, images=images)

if __name__ == "__main__":
    app.run(debug=True)
