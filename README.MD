# Yieldify Backend
![logo](./logo.png "Title")

### Disclaimers
This product includes GeoLite2 data created by MaxMind, available from
https://dev.maxmind.com/geoip/geoip2/geolite2/

## Getting Started

### Installing Dependencies

#### Python 3.8

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment
If you have `virtualenv` installed proceed to the next step otherwise, to install `virtualenv` enter the following
command in your terminal:
```bash
$ pip3 install virtualenv
```

Once installed, setup your virtual environment using the following steps:

 

```bash
$ cd yieldify/
$ virtualenv env
$ source env/bin/activate
```

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Psycopg2](https://pypi.org/project/psycopg2/) Psycopg2 is the most popular python driver for PostgreSQL.

- [GeoLite2](https://dev.maxmind.com/geoip/geoip2/geolite2/) This product includes GeoLite2 data created by MaxMind.

## Database Setup
With Postgres running, enter the following commands within terminal run (substitue <> with your own directories):
```bash
$ createdb yieldify
$ python3 create_tables.py --table='yieldifydb'
$ python3 etl.py --directory=<DATA_LOCATION> --archive=<PROCESSED_DATA_DROP> --database=yieldifydb
```

## Running the server

From within the `yieldify` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app
flask run
```

Setting the `FLASK_APP` variable to `app` directs flask to use the `app` directory and the `__init__.py` file to find the application. 



## Testing
There are a total of `10` tests which can be found `/yieldify/test_app.py`. These tests are designed to pick up edge cases
to ensure the application runs with the correct behaviour for each endpoint.

To run the tests, navigate to the `yieldify` directory and run:
```
$ dropdb yieldify_test
$ python3 create_tables.py --table='yieldifydb_test'
$ python3 etl.py --directory=<DATA_LOCATION> --archive=<PROCESSED_DATA_DROP> --database=yieldifydb_test
$ python test_app.py
```

# API Documentation
The Yieldify API is organised around `REST`. The API returns `JSON-encoded` responses using the standard HTTP response codes.
 
Below, you will find all existing endpoints with the accepted method usage and how to work with them.

#### Base URL
As this is a locally hosted version running flask natively, it can only be access when flask is running. To construct 
a request you must use 'curl' or a 3rd party API sevice like Postman and use the following address:
*http://127.0.0.1:5000/*

### Endpoints
Resources and methods:

|  Endpoint location | GET  | POST|DELETE|
|---         |:---:|:---:|:---:
| /stats/browser |✓  |x  |x  |
| /stats/os|✓  | x  | x  |
| /stats/device   | ✓  |  x |  x |



<details>
  <summary markdown="span"> GET /stats/browser</summary>
    Description: return browser stats from Postgres database with optional parameters (start_date, end_date):
    
   
  ```
$ curl -X GET 'http://127.0.0.1:5000/stats/browser?start_date=2014-10-12&end_date=2014-10-13'
   ```
    
- Returns a dictionaries of the top 5 browser.

- Request headers: None

- Output: 
    - start_date: str
    - end_date: str
    - result: dict
    - success: boolean
    
    Example response:
    ```JSON
    {"end_date": "2014-10-13", 
     "result": {
        "Chrome":100,
        "Firefox":45,
        "IE":55,
        "Mobile Safari":247,
        "Safari":64},
     "start_date":"2014-10-12",
     "success":true}
    ```
  #### Errors
  If you try to use a method not specified above you will get the following error:
  
  ```
  $ curl -X POST 'http://127.0.0.1:5000/stats/browser?start_date=2014-10-12&end_date=2014-10-13'
  {"error":405,"message":"method not allowed","success":false}

  ```
  
  If you specify a date range outside of the date column range it will return an error:
  
  ```
  curl -X GET 'http://127.0.0.1:5000/stats/browser?start_date=2020-10-12&end_date=2020-10-13'
   
  {"error":400,"message":"bad request","success":false}
  ```
</details>

<details>
  <summary markdown="span"> GET /stats/os</summary>
    Description: return operating system stats from Postgres database with optional parameters (start_date, end_date):
    
   
  ```
$ curl -X GET 'http://127.0.0.1:5000/stats/os?start_date=2014-10-12&end_date=2014-10-13'
   ```
    
- Returns a dictionaries of the top 5 operating systems by user usage.

- Request headers: None

- Output: 
    - start_date: str
    - end_date: str
    - result: dict
    - success: boolean
    
    Example response:
    ```JSON
    {
      "end_date":"2014-10-13",
      "result":{
          "Android":56,
          "Linux":7,
          "Mac OS X":78,
          "Windows":172,
          "iOS":269},
      "start_date":"2014-10-12",
      "success":true
    }
    ```
  #### Errors
  If you try to use a method not specified above you will get the following error:
  
  ```
  $ curl -X POST 'http://127.0.0.1:5000/stats/os?start_date=2014-10-12&end_date=2014-10-13'
  {"error":405,"message":"method not allowed","success":false}

  ```
  
  If you specify a date range outside of the date column range it will return an error:
  
  ```
  curl -X GET 'http://127.0.0.1:5000/stats/os?start_date=2020-10-12&end_date=2020-10-13'
   
  {"error":400,"message":"bad request","success":false}
  ```
</details>

<details>
  <summary markdown="span"> GET /stats/device</summary>
    Description: return device stats from Postgres database with optional parameters (start_date, end_date):
    
   
  ```
$ curl -X GET 'http://127.0.0.1:5000/stats/device?start_date=2014-10-12&end_date=2014-10-13'
   ```
    
- Returns a dictionaries of the top 5 devices by distinct user usage.

- Request headers: None

- Output: 
    - start_date: str
    - end_date: str
    - result: dict
    - success: boolean
    
    Example response:
    ```JSON
    {
    "end_date":"2014-10-13",
    "result":{
      "Mac":78,
      "Other":183,
      "Samsung GT-I9505":7,
      "iPad":175,
      "iPhone":94
    },
    "start_date":"2014-10-12",
    "success":true
    }
    ```
  #### Errors
  If you try to use a method not specified above you will get the following error:
  
  ```
  $ curl -X POST 'http://127.0.0.1:5000/stats/device?start_date=2014-10-12&end_date=2014-10-13'
  {"error":405,"message":"method not allowed","success":false}

  ```
  
  If you specify a date range outside of the date column range it will return an error:
  
  ```
  curl -X GET 'http://127.0.0.1:5000/stats/device?start_date=2020-10-12&end_date=2020-10-13'
   
  {"error":400,"message":"bad request","success":false}
  ```
</details>