# Description
This is tasks for Akvelon Python SDE candidate

This is Django + PostgreSQL project

The project available [here](https://akvelon-python-internship.herokuapp.com/swagger/)

description | path | detail
--- | --- | ---
REST API registration | [/rest-auth/registration/](https://akvelon-python-internship.herokuapp.com/rest-auth/registration/) | allows both cookie and token based authentication
Swagger | [/swagger/](https://akvelon-python-internship.herokuapp.com/swagger/) 
|CRUD information about your account | [/rest-auth/user/](http://akvelon-python-internship.herokuapp.com/rest-auth/user/) | requires registration/authentication.
CRUD on your transactions | [/api/v1/transactions/](http://akvelon-python-internship.herokuapp.com/api/v1/transactions/) or  /api/v1/transactions/\<id\> | requires registration/authentication. Allows filtering(open the link)|
your transactions grouped by date | [/api/v1/transactions/group_by_day/](http://akvelon-python-internship.herokuapp.com/api/v1/transactions/group_by_day/) | cumulative money gain per date. Allows filtering(open the link)
| find Nth fibonacci number |[/api/v1/fibonacci/](http://akvelon-python-internship.herokuapp.com/api/v1/fibonacci/)

## View all users data:
For this you need to ented as an admin and go to  [/admin/core/transaction/](https://akvelon-python-internship.herokuapp.com/admin/core/transaction/)

login | password
--- | ---
admin| admin

# fibonacci

function itself located in [`core/utils.py`](core/utils.py)  
also there's a [endpoint for fibonacci number](http://akvelon-python-internship.herokuapp.com/api/v1/fibonacci/)

# Run project
## With docker:
1. run in the project folder
```
docker-compose up --build
```
## locally:
1. set environment variables
```
SECRET_KEY=your_key_here
DEBUG=TRUE
```
2. then run in the project folder
```bash
pip install -r requirements.txt
python manage.py runserver
```

# Run tests
```
pip install -r requirements.txt
python manage.py test
```
Tests are in [`core/tests.py`](core/tests.py)  