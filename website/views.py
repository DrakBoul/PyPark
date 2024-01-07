from flask import Blueprint, render_template, Response, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User, ParkingSpot
from . import db
import serial
import time
ser = serial.Serial('COM3', 9600)
ser.close()
ser = serial.Serial('COM3', 9600)





views = Blueprint('views', __name__)

# when navigated to views route the 'home' function will run

@views.route('/', methods=['POST', 'GET'])
@login_required
def home():
    if request.method == 'POST':
        book_parking_spot()
        get_uid()
        print("arduino was sent users UID")

    check_serial_data()
    

    return render_template("home.html", user=current_user)

@login_required
def book_parking_spot():
    parking_spot = ParkingSpot.query.first()

    if parking_spot is None:
        # Create a default parking spot
        parking_spot = ParkingSpot(name='Default Parking Spot')
        db.session.add(parking_spot)
        db.session.commit()

    # Check if the parking spot is available
    if parking_spot.owner is None:
        # Book the parking spot for the current user
        parking_spot.owner = current_user
        db.session.commit()
        flash("Parking spot booked successfully!", category='success')
    else:
        flash("Parking spot is already booked.", category='error')

    return redirect(url_for('views.home'))

def get_uid():
    user = current_user 
    if user:
        uid= user.UID
        send_uid_to_arduino(uid)
        print(uid)
    return Response(status=200)

def send_uid_to_arduino(uid):
    time.sleep(2)  
    ser.write(uid.encode("utf-8"))
    ser.flush()

def check_serial_data():
    
    while ser.in_waiting:
        serial_data = ser.readline().decode("utf-8").strip()
        print(serial_data)

        # Check if the spot is now open
        if serial_data == "1":
            # Update the database indicating that the spot is now open
            parking_spot = ParkingSpot.query.first()
            parking_spot.owner = None
            db.session.commit()
            flash("Parking spot is now open!", category='success')
        if serial_data == "0":
            parking_spot = ParkingSpot.query.first()
            parking_spot.owner = 'unknown'
            db.session.commit()
            flash("Parking spot is now open!", category='success')
