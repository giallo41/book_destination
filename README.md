# Data Science Task 

----------------------

created by Sue Hun Jung giallo.hos@gmail.com

----------------------

## Goal 


Identify users that will eventually book a trip to an advertised destination


# [ Instruction ]

### 1. Files and Folder 

```
project
│   instruction.md
│   model.ipynb
|   preprocessing.ipynb
│   readme.md
│   requirements.txt
│
└─── data
│   │   events.csv 
│   │   events.parquet 
│   └─  iata.csv
│   
└─── source
    └─  utils.py   
```

## 2. requirements.txt 
#### Requirements

Model works in Python 3.7 or above version
```
pip install -r requirements.txt
```

## 2. How to run 

[1] Data pre-proessing and eda

```
preprocessing.ipynb 
```

[2] Line by line running jupyter notebook

```
model.ipynb 
```




----------------------

# [ Taks Results ]

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

```
(1) Day of week for each datetime columns
(2) 'Hours' of 'ts'
(3) 'Days' for each datetime columns
(4) 'trip_duration' in days
```

[4] Add distance in km (haversine distance)


### 3. Save Featured data

To keep the datatype, featured data save to parquet


### 4. Train / Test Split
```
A. Target value is highly imbalanced. (1808 / 45177) 3.8%
B. The ratio of booked users / searched users is slightly better than the target value ratio. (1804 / 29361) 5.7%
C. Activity ratio of booked users / searched users is much better. (9486 / 37499) 20.2%
```

#### Train / Test Split should have the similar distribution
```
[1] Select randomly booked user in 20% and searched users in 20% as Test user
[2] Split Train / Test data based on train / test userid
```

### 5. Feature Selection

##### Select important features using tree based classfier 

##### 3 important features for decision are
```
[1] 'diff_ts' - time difference between actions for unique user
[2] 'act_count' - number of activity for each unique users
[3] 'trip_distance' - Trip distance between origin in destination in km
```

### 6. Model Selection

Using cross_val_score, RandomForest Classifier is best score for training datasets 