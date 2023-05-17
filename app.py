from flask import Flask,render_template,url_for,redirect,request,flash
from forms import LoginForm,RegisterForm
from werkzeug.security import check_password_hash, generate_password_hash
from claud import execute

app=Flask(__name__)
app.config["SECRET_KEY"] = "9e5734eb4a542802b7c24415"


@app.route("/")
def home_page():
  return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register_page():
    form = RegisterForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user_to_check = db.execute(
                "SELECT * FROM users WHERE username = ?", form.username.data
            )
            if len(user_to_check) == 1:
                category = "danger"
                flash(["Please use different username !"], category)
                return render_template("register.html", form=form)
            else:
                # INSERT the new user into users, storing a hash of the user’s password, not the password itself.
                hash = generate_password_hash(
                    form.password.data, method="pbkdf2:sha256", salt_length=8
                )
                db.execute(
                    "INSERT INTO users (username,hash,email) VALUES (?,?,?)",
                    form.username.data,
                    hash,
                    form.email.data,
                )

                # Query database for id
                rows = db.execute(
                    "SELECT * FROM users WHERE username = ?", form.username.data
                )
                # Remember which user has logged in
                session["user_id"] = rows[0]["id"]
                # Redirect user to home page
                return redirect(url_for("home_page"))
        if form.errors != {}:
            for error_msg in form.errors.values():
                category = "danger"
                flash(error_msg, category)
            return render_template("register.html", form=form)
    else:
        return render_template("register.html", form=form)
      

@app.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            # Query database for id
            rows = db.execute(
                "SELECT * FROM users WHERE username = ?", form.username.data
            )
            # Ensure username exists and password is correct
            if len(rows) != 1 or not check_password_hash(
                rows[0]["hash"], form.password.data
            ):
                category = "danger"
                flash(["Incorrect password or username please try again !"], category)
                return render_template("login.html", form=form)
            else:
                # Remember which user has logged in
                #session["user_id"] = rows[0]["id"]
                # Redirect user to home page

                return redirect(url_for("home_page"))
    else:
        return render_template("login.html", form=form)

if __name__=="__main__":
  app.run(host="0.0.0.0", debug=True)