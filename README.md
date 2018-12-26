 # Zombie Survivor Social Network
  Is an API REST for resource sharing between survivors in chaotic scenario
  This API it was written in Python with Django and Django rest framework
  ## To run the API follow this steps
  ### Windows
  `ZSSN/zssn_venv/bin/activate` (for activate the virtualenv)

  `python pip -m install -r requirements.txt`(for download the dependencies)

  `cd zssn`

  `python manage.py migrate`
  
  `python manage.py makemigrations`

  `python manage.py runserver` 
	
  `python manage.py test` (run the tests)

  ### Linux
  `source zssn_venv/bin/activate` (for activate the virtualenv)

  `pip install -r requirements.txt`(for download the dependencies)

  `cd zssn`

  `make migrate`
  
  `make runserver`
  
  `make test` (to run the tests)

### API Endpoints

 - /survivor for list all survivors and **POST** them
 - /survivor/reports for **GET** all reports


   
   
   
   
   
   

   

