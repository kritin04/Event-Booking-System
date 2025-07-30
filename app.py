from flask import Flask, render_template, request, redirect, url_for, session
from db_config import get_db_connection
import psycopg2

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for session management

# Route: Home
@app.route("/", methods=["GET", "POST"])
@app.route("/")
def index():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch Users
    cursor.execute("SELECT * FROM Users;")
    users = cursor.fetchall()

    # Fetch Events
    cursor.execute("SELECT * FROM Event;")
    events = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("index.html", users=users, events=events)


# Route: Add User (Separate Route, Not Necessary if Handled Above)
@app.route("/add_user", methods=["GET", "POST"])
def add_user():
    if request.method == "POST":
        fname = request.form["fname"]
        lname = request.form["lname"]
        state = request.form["state"]
        city = request.form["city"]
        dob = request.form["dob"]
        ref_uid = request.form.get("ref_uid", None)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Users (Fname, Lname, State, City, DOB, Ref_UID) VALUES (%s, %s, %s, %s, %s, %s)",
            (fname, lname, state, city, dob, ref_uid),
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for("index"))

    return render_template("add_user.html")

# Route: View Events
@app.route("/events")
@app.route("/events")
def events():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Event;")
    events = cursor.fetchall()  # Fetch all events from the database
    cursor.close()
    conn.close()
    return render_template("events.html", events=events)


# Route: Book Ticket
# Route: Book Ticket
@app.route("/book/<int:event_id>", methods=["GET", "POST"])
def book(event_id):
    if request.method == "POST":
        # Handle ticket booking form submission
        seat_no = request.form["seat_no"]
        price = request.form["price"]
        uid = session.get("uid")  # Get the logged-in user's ID from the session

        if not uid:
            return redirect(url_for("index"))  # Redirect to home if not logged in

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Tickets (UID, SeatNo, TPrice, EventID) VALUES (%s, %s, %s, %s)",
            (uid, seat_no, price, event_id)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("events"))  # Redirect to events page after booking

    # For GET requests, fetch event details
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT * FROM Event WHERE EventID = %s", (event_id,))
    event = cursor.fetchone()  # Fetch the event as a dictionary
    cursor.close()
    conn.close()

    if not event:
        return "Event not found", 404  # Show 404 error if event doesn't exist

    return render_template("book_ticket.html", event=event)  # Render booking page


# Route: Logout
@app.route("/logout")
def logout():
    session.pop("uid", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)

