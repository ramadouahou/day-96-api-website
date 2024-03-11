import time
import requests
import smtplib
from flask import Flask, request, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
import datetime as dt


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

YOUR_GMAIL = "YOUR_GMAIL"
YOUR_PASSWORD = "YOUR_PASSWORD"
emails = []


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    email = request.form.get("email")
    emails.append(email)
    return redirect(url_for("home"))


def send_email():
    print("sending email...")

    url = "https://v2.jokeapi.dev/joke/Any"
    response = requests.get(url)

    try:
        joke = response.json()["joke"]
        message = joke
    except KeyError:
        setup = response.json()["setup"]
        delivery = response.json()["delivery"]
        message = f"{setup}\n{delivery}"

    try:
        for recipient in emails:
            with smtplib.SMTP("smtp.gmail.com", port=587, timeout=30) as connection:
                connection.starttls()
                connection.login(user=YOUR_GMAIL, password=YOUR_PASSWORD)
                connection.sendmail(
                    from_addr=YOUR_GMAIL,
                    to_addrs=recipient,
                    msg=f"Subject:Here is your daily dose of joke!\n\n{message}"
                )
    except Exception as e:
        print(f"Error sending email: {e}")


if __name__ == "__main__":
    while True:
        current_hour = dt.datetime.now().hour
        current_minute = dt.datetime.now().minute

        if current_hour == 7 and current_minute == 0:
            send_email()

        time.sleep(60)
