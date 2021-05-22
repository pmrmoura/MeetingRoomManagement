# Meeting Rooms

Built using Django Rest Framework, MeetingRoomManagement is an API where each authenticated employee(user) is able to check each room’s availability, book or cancel a reservation.

## Initial instructions

### Run the app

The solution is presented into a Docker environment and you can use it to run the server locally following the following step on the root directory:

    docker-compose up --build
    
After the containers are up, you can run this command to create a new bash session, where you can run the other commands

### Create container bash session

    docker exec -it meetingroomanager bash

Now, you can run any of the following commands

### Run the tests

    python manage.py test
  
### Run linter
    flake8

# Authentication

## Registration

Before using the API you should registrate yourself. Each registered user will be an Employee.

### Request

`POST /auth/register/`

    curl --location --request POST 'http://localhost:8080/auth/register/' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "username": "example",
        "password": "examplepassword"
    }'

### Response

    {
      "id":1,
      "username":"example",
      "token":"5cc92ce7b7bad179a270739249626b55ae649bdb"
    }

## Login

### Request

`POST /auth/login/`

    curl --location --request POST 'http://localhost:8080/auth/login/' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "username": "example",
        "password": "examplepassword"
    }'

### Response

     {
        "auth_token": "5cc92ce7b7bad179a270739249626b55ae649bdb",
        "created": "YYYY-MM-DD hh:mm:ss[.nnnnnnn] [+|-]hh:mm"
     }

## Logout

### Request

`DELETE /auth/logout/`

    curl --location --request DELETE 'http://localhost:8080/auth/logout/' \
    --header 'Authorization: Token 5cc92ce7b7bad179a270739249626b55ae649bdb' \
    --data-raw ''

### Response

    {
      "message": "User logged out"
    }

## Note:

You should put the token you received either on Login or Registration in the other following requests for it be authorized
    
# Meetings Rooms

## Create a meeting room

### Request

`POST /rooms/`

    curl --location --request POST 'http://localhost:8080/rooms/' \
    --header 'Authorization: Token 5cc92ce7b7bad179a270739249626b55ae649bdb' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "name": "Class47"
    }'

### Response

    {
      "id": 1,
      "name": "Class47"
    }

## List meeting rooms

### Request

`GET /rooms/`

    curl --location --request GET 'http://localhost:8080/rooms/' \
    --header 'Authorization: Token 5cc92ce7b7bad179a270739249626b55ae649bdb' \
    --data-raw ''

### Response

    [
      {
          "id": 1,
          "name": "Class46"
      },
      {
          "id": 2,
          "name": "Class47"
      }
    ]

## Delete meeting room

### Request

`DELETE /rooms/:id/`

     curl --location --request DELETE 'http://localhost:8080/rooms/2/' \
    --header 'Authorization: Token 5cc92ce7b7bad179a270739249626b55ae649bdb' \
    --data-raw ''

### Response

    {}
    
# Reservations

## Create reservation

### Request

`POST /reservation/`

    curl --location --request POST 'http://localhost:8080/reservation/' \
    --header 'Authorization: Token 5cc92ce7b7bad179a270739249626b55ae649bdb' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "title": "Deciding",
        "from_date": "2021-12-04T23:20:00Z",
        "to_data": "2021-12-05T23:20:03Z",
        "room": 1,
        "employees": [1]
    }'

### Response

    {
      "id": 1,
      "title": "Meeting Example",
      "from_date": "2021-12-01T23:20:00Z",
      "to_data": "2021-12-02T23:20:03Z",
      "room": 1,
      "employees": [
          1
      ]
    }

## List reservations

### Request

`GET /reservation/`

    curl --location --request GET 'http://localhost:8080/reservation/' \
    --header 'Authorization: Token 5cc92ce7b7bad179a270739249626b55ae649bdb' \
    --data-raw ''

### Response

    [
      {
          "id": 1,
          "title": "Deciding",
          "from_date": "2021-12-14T23:20:00Z",
          "to_data": "2021-12-14T23:20:03Z",
          "room": 1,
          "employees": [
              1
          ]
      },
      {
          "id": 2,
          "title": "Example",
          "from_date": "2021-12-14T11:20:00Z",
          "to_data": "2021-12-14T12:20:00Z",
          "room": 1,
          "employees": [
              1
          ]
      }
]

### You can filter reservations using the following params:
    employee_id
    meeting_room_id
    
  You can use both of them combined or just one.
  
#### Request example using filters
    curl --location --request GET 'http://localhost:8080/reservation/?employee_id=1&meeting_room_id=4' \
    --header 'Authorization: Token 5cc92ce7b7bad179a270739249626b55ae649bdb' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "title": "Deciding",
            "from_date": "2021-12-10T16:03:00Z",
            "to_data": "2021-14-T11:00:00Z",
            "room": 1,
            "employees": [
                1
            ]
    }'

## Delete reservation

### Request

`DELETE /reservation/:id/`

     curl --location --request DELETE 'http://localhost:8080/reservation/1/' \
    --header 'Authorization: Token ffaaebd16ea774f82c3990efcd7a74470a31212f' \
    --data-raw ''

### Response

    {}
 
# Observations
- Implemented a Github Action named CI to run all the test after each commit pushed to any branch
