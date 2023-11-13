#### Note that:
- a user can only have one active booking at a time (user 1to1 with booking)
- maybe add default price for parking slots and when a rule is active overwrites that (not implemented)


### CURD enpoints
http://localhost:8000/ParkingApp/api/
- parkowner/
- users/
- park/
- parkdetails/
- floors/
- parkingslots/
- parkingslotrules/
- bookings/
- credentials/

### Story endpoints, what to include in request body:

**create bookings**: check if a rule is active and updates price for the specific time frame, else checks if the booking can be made for that time
- user
- booking_start_date(iso format)
- booking_end_date(iso format)
- parking_slot (id) 



#### for GET, UPDATE, DELETE with pk: http://localhost:8000/ParkingApp/api/users/pk
