from flask import Blueprint, render_template, Response, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User, ParkingSpot
from . import db
import serial
import time
ser = serial.Serial('COM3', 9600)
ser.flush
ser.close()
ser = serial.Serial('COM3', 9600)

not_occupied = True
views = Blueprint('views', __name__)

# when navigated to views route the 'home' function will run

@views.route('/', methods=['POST', 'GET'])
@login_required
def home():
    if request.method == 'POST':
        book_parking_spot()
        

    check_serial_data()
    

    return render_template("home.html", user=current_user)

@login_required
def book_parking_spot():
    global not_occupied
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
        get_uid()
        not_occupied = False
        print("arduino was sent users UID")
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
            not_occupied = True
            flash("Drake's Parking Space is Now Open!", category='success')
        if serial_data == "0":
            unknown_user = User.query.filter_by(email='unknown@example.com').first()
            if not unknown_user:
                unknown_user = User(email='unknown@example.com', first_name='Unknown')
                db.session.add(unknown_user)
                db.session.commit()
            parking_spot = ParkingSpot.query.first()
            parking_spot.owner = unknown_user
            db.session.commit()
            not_occupied = False
            flash("Parking Space is taken!", category='error')



























# from flask import Blueprint, render_template, Response, request, flash, redirect, url_for
# from flask_login import login_required, current_user
# from .models import User, ParkingSpot
# from . import db
# import serial
# import time

# # Some function has to prevent new booking from overwriting previous ones.
# # Need to find out where to flush so that serial monitor doesnt pick up bogus info.
# # Find out where i need to release parking space from a user


# not_occupied = True
# views = Blueprint('views', __name__)

# # when navigated to views route the 'home' function will run

# @views.route('/', methods=['POST', 'GET'])
# @login_required
# def home():
#     global ser
#     ser = serial.Serial('COM3', 9600)
#     ser.flush()
#     not_occupied = check_serial_data()
#     if request.method == 'POST':
#         book_parking_spot()
#     ser.close()
#     return render_template("home.html", user=current_user)

# @login_required
# def book_parking_spot():
#     parking_spot = ParkingSpot.query.first()
#     # Check if the parking spot is available
#     if  not_occupied and parking_spot.owner is None:
#         # Book the parking spot for the current user
#         parking_spot.owner = current_user
#         db.session.commit()
#         get_uid()
#         flash("Parking spot booked successfully!", category='success')
#     else:
#         flash("Parking spot is Taken.", category='error')

#     return redirect(url_for('views.home'))

# def get_uid():
#     user = current_user 
#     if user:
#         uid= user.UID
#         send_uid_to_arduino(uid)
#         print(uid)
#     return Response(status=200)

# def send_uid_to_arduino(uid):
#     time.sleep(2)  
#     ser.flush()
#     ser.write(uid.encode("utf-8"))

# def check_serial_data():
#     parking_spot = ParkingSpot.query.first()

#     if parking_spot is None:
#         # Create a default parking spot
#         print("created parking spot")
#         parking_spot = ParkingSpot(name='Default Parking Spot')
#         db.session.add(parking_spot)
#         db.session.commit()

#     while ser.in_waiting:
#         serial_data = ser.readline().decode("utf-8").strip()
#         print(serial_data)

#         # Check if the spot is now open
#         if serial_data == "1" and parking_spot.owner is None:
#             not_occupied = True
#             print("parking spot is open.")
#             try:
#                 parking_spot.owner = None
#             except:
#                 pass
#             return True
#         if serial_data == "0":
#             not_occupied = False
#             print("parking spot is taken.")
    
#             return False
#     return True

# # def check_serial_data():
    
#     # while ser.in_waiting:
#     #     serial_data = ser.readline().decode("utf-8").strip()
#     #     print(serial_data)

#     #     # Check if the spot is now open
#     #     if serial_data == "1":
#     #         # Update the database indicating that the spot is now open
#     #         try:
#     #             parking_spot = ParkingSpot.query.first()
#     #             parking_spot.owner = None
#     #             db.session.commit()
#     #         except:
#     #             pass
#     #         flash("Parking spot is now open!", category='success')
#     #     if serial_data == "0":
#     #         parking_spot = ParkingSpot.query.first()
#     #         parking_spot.owner = 'unknown'
#     #         db.session.commit()
#     #         flash("This Spot is Taken.", category='error')
