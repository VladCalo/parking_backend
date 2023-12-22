#### Note that:
- jwt not implemented yet
- a user can only have one active booking at a time (user 1to1 with booking)
- updates are full updates not partial 
- dates are in ISO format 
  - ex: 2023-01-01T00:00:00.000Z

- to access the admin page of Django app where you can add entries in tables:
  - first install req.txt
  - "cd" to where manage.py is located
  - ```bash
    python3 manage.py runserver
    ```
  - http://localhost:8000/admin/ and login with admin/admin


### Endpoints
http://localhost:8000/ParkingApp/

- **/login/** (POST method)
  - email
  - password

- **/park-owner/**
  - C
    - first_name
    - last_name
    - email
    - password
  - R

- **/park-owner/<int:pk>/**
  - R
  - U
    - first_name
    - last_name
    - email
    - password
  - D

- **/users/**
  - C
    - credentials
    - first_name
    - last_name
    - number_plate
    - vehicle_type(marca + model ex: "Dacia Logan")
    - verified (bool)
  - R

- **/users/<int:pk>/**
  - R
  - U
    - credentials
    - first_name
    - last_name
    - number_plate
    - vehicle_type(marca + model ex: "Dacia Logan")
    - verified (bool)
  - D

- **/credentials/**
  - C
    - email
    - password
  - R

- **/credentials/<int:pk>/**
  - R
  - U
    - email
    - password
  - D

- **/park/**
  - C
    - park_owner
    - total_spots
    - no_floors
    - park_details
  - R

- **/park/<int:pk>/**
  - R
  - U
    - park_owner
    - total_spots
    - no_floors
    - park_details
  - D

- **/park-details/**
  - C
    - address
    - latitude (decimal)
    - longitude (decimal)
    - height_limit (int)
    - weigh_limit (int)
  - R

- **/park-details/<int:pk>/**
  - R
  - U
    - address
    - latitude (decimal)
    - longitude (decimal)
    - height_limit (int)
    - weight_limit (int)
  - D

- **/floors/**
  - C
    - park
    - floor_number
  - R

- **/floors/<int:pk>/**
  - R
  - U
    - park
    - floor_number
  - D

- **/parking-slots/**
  - C
    - floor
    - slot_number
    - has_charger
    - physical_available
    - standard_price
  - R

- **/parking-slots/<int:pk>/**
  - R
  - U
    - floor
    - slot_number
    - has_charger
    - physical_available
    - standard_price
  - D

- **/parking-slots/available/**
  - R
    - has_charger(bool)

- **/parking-slot-rules/**
  - C
    - parking_slot
    - date_start_rule
    - date_end_rule
    - price
  - R

- **/parking-slot-rules/<int:pk>/**
  - U
    - parking_slot
    - date_start_rule
    - date_end_rule
    - price
  - D

- **/parking-slot-rules/by-pk/<int:pk>/**
  - R (sorry retrieve by pk is separate, dev complication)

- **/bookings/**
  - C
    - user
    - parking_slot
    - booking_start_date (ISO format)
    - booking_end_date (ISO format)
  - R

- **/bookings/<int:pk>/**
  - R
  - U
    - user
    - new_start_date (ISO format)
    - new_end_date (ISO format)
    - new_parking_slot (it can also be the same parking slot)
  - D
