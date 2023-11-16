#### Note that:
- a user can only have one active booking at a time (user 1to1 with booking)
- maybe add default price for parking slots and when a rule is active overwrites that (not implemented)


### Endpoints
http://localhost:8000/ParkingApp/
- **/park-owner/**
  - C
  - R

- **/park-owner/<int:pk>/**
  - R
  - U
  - D

- **/users/**
  - C
  - R

- **/users/<int:pk>/**
  - R
  - U
  - D

- **/credentials/**
  - C
  - R

- **/credentials/<int:pk>/**
  - R
  - U
  - D

- **/park/**
  - C
  - R

- **/park/<int:pk>/**
  - R
  - U
  - D

- **/park-details/**
  - C
  - R

- **/park-details/<int:pk>/**
  - R
  - U
  - D

- **/floors/**
  - C
  - R

- **/floors/<int:pk>/**
  - R
  - U
  - D

- **/parking-slots/**
  - C
  - R

- **/parking-slots/<int:pk>/**
  - R
  - U
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
    - new_start_date
    - new_end_date
    - new_parking_slot (it can also be the same parking slot)
  - D
