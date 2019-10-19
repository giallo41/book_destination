# Data Science Task 

## Goal 
Identify users that will eventually book a trip to an advertised destination


### 1. Data pre-Processing 

[1] Dropping NaN data in 'date_from' and 'date_to'<br>

    - relatively small compare to original data size 
    - 'book' event won't work without a 'date_from' and 'date_to'. This data is wrong some way 

[2] Drop duplicated of iata_code in 'iata.csv', because iata_code is not unique<br>


### 2. Feature Engineering 

[1] Add number of activities of uninque user<br>

    - 'act_count' is number of activity for each unique users. 

[2] Add time difference between actions for unique user<br>

[3] Add time feature of datetime columns<br>

- Usually user activities and trip plans shows seasonality
- This dataset has short period of time, so I added the

(1) Day of week for each datetime columns<br>
(2) 'Hours' of 'ts'<br>
(3) 'Days' for each datetime columns<br>
(4) 'trip_duration' in days<br>

[4] Add distance in km (haversine distance)

