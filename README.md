
# Zombie Survivor Social Network

It is an API REST for resource sharing between survivors in chaotic scenario.

This API was written in Python with Django and Django Rest Framework.

The  [Postman](https://www.getpostman.com/)  program was used to do some manual tests.

## [](https://github.com/luchiago/zssn#to-run-the-api-follow-this-steps)To run the API follow this steps

### [](https://github.com/luchiago/zssn#linux)Linux commands

#### [](https://github.com/luchiago/zssn#in-the-terminal-in-the-project-folder)In the terminal, enter the root folder of the project

`python3 -m venv env`  (to create the virtualenv)

`source env\bin\activate`  (to activate the virtualenv)

`pip install -r requirements.txt`  (to download the dependencies)

`cd zssn` (where there are the manage.py)

`make migrate` (to update the database and migrations)

`make runserver` (to run the project)

`make test`  (to run the tests)

### [](https://github.com/luchiago/zssn#api-endpoints)API Endpoints

-   /survivor/ for list all survivors with  *GET*  method and create them with  *POST*  method JSON Model:  `{ "name" : <str>, "age" : <int>, "gender" : <str>, "last_location_longitude" : <str>, "last_location_latitude" : <str>, "water" : <int>, "food" : <int>, "medication" : <int>, "ammunition" : <int> }`
    
-   /survivor/id/ to list the details of the survivor with  *GET*  method
    
-   /reports/ to generate reports with  *GET*  method
    
-   /updatelocation/id/ to update location of survivor with  *PATCH*  method JSON Model:  `{ "last_location_longitude" : <str>, "last_location_latitude" : <str> }`
    
    Example location Latitude: 80º 21' 25'' N" E (0 to 90 N/S ) Longitude: 172º 23' 23'' E (0 to 180 W/E)
    
-   /infected/id/ to report a survivor as infected with  *PATCH*  method JSON Model:  `{ "reportx" : <int:id> }`
    
    where "x" is the number of report and int:id is the id of the whistleblower survivor
    
-   /trade/ to make the trade between items of survivors JSON Model:  `{ "survivor1_id" : id, "items1_trade": {"type" : amount}, "survivor2_id": id, "items2_trade": {"type" : amount} }`
    
    where "type" is the item e "amount" is the amount of the item (e.g "water" : 5)
