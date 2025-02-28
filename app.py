from flask import Flask, request, redirect, url_for, render_template
import pandas as pd

app = Flask(__name__)

# Path to the Excel file for storing registered users
EXCEL_FILE = "registered_users.xlsx"


# ✅ Route for Registration Page
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        password = request.form.get("password")

        new_user = {
            "First Name": [firstname],
            "Last Name": [lastname],
            "Email": [email],
            "Password": [password],
        }

        df_new_user = pd.DataFrame(new_user)

        try:
            df_existing = pd.read_excel(EXCEL_FILE)
            df_updated = pd.concat([df_existing, df_new_user], ignore_index=True)
        except FileNotFoundError:
            df_updated = df_new_user

        df_updated.to_excel(EXCEL_FILE, index=False)
        return redirect(url_for("success"))

    return render_template("register.html")

# ✅ Route for Home Page
@app.route("/")
def home():
    return render_template("home.html")

# ✅ Route for Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        try:
            df_users = pd.read_excel(EXCEL_FILE)
            user = df_users[(df_users["Email"] == email) & (df_users["Password"] == password)]

            if not user.empty:
                return redirect(url_for("home"))
            else:
                return "Invalid login credentials. Try again."
        except FileNotFoundError:
            return "No registered users found."

    return render_template("login.html")


# ✅ Route for Index Page
@app.route("/index")
def index():
    return render_template("index.html")

# ✅ Route for Exit Page
@app.route("/exit")
def exit_page():
    return render_template("exit.html")

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
