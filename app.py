from flask import Flask, request, redirect, url_for, render_template
import pandas as pd

app = Flask(__name__)

# Path to the Excel file
EXCEL_FILE = "registered_users.xlsx"

# Route for the registration page
@app.route("/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Get form data
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        password = request.form.get("password")

        # Create a dictionary with the form data
        new_user = {
            "First Name": [firstname],
            "Last Name": [lastname],
            "Email": [email],
            "Password": [password],
        }

        # Convert the dictionary to a DataFrame
        df_new_user = pd.DataFrame(new_user)

        try:
            # Try to read the existing Excel file
            df_existing = pd.read_excel(EXCEL_FILE)
            # Append the new user to the existing data
            df_updated = pd.concat([df_existing, df_new_user], ignore_index=True)
        except FileNotFoundError:
            # If the file doesn't exist, create a new DataFrame
            df_updated = df_new_user

        # Save the updated DataFrame to the Excel file
        df_updated.to_excel(EXCEL_FILE, index=False)

        # Redirect to a success page or the same page
        return redirect(url_for("success"))

    # Render the registration form
    return render_template("register.html")

# Route for the success page
@app.route("/success")
def success():
    return "Registration Successful! Thank you for signing up."

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)