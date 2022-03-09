# carpark_availability

Stack used:
Python Flask (backend) + SQLite3 (DB)

Flask setup:
1) Navigate to the directory where the app.py is stored.
2) Open terminal and type "python app.py" to launch the Flask app.

DB setup:
1) DB and the User table will be automatically initated, the moment when the .py file is run.
2) If you want to manually look at the DB contents, open Terminal and navigate to the directory where the DB is stored.
3) Type "sqlite3 carpark.db", to enter SQL mode for the DB created.
4) Execute any SQL lines needed. For example, "SELECT * FROM USER" shows all contents in user table.
5) Type ".exit" or CTRL-C to terminal the SQL mode.

POSTMAN setup:
1) A pre-made postman collection has been created for easier interaction/testing with the API.
2) Go to Postman app and import carpark_availability.postman_collection.json.
3) 4 ready tabs will be found in the collection, and values have been added into the route, headers and body.
4) Do note that the JWT token expire in 60min and there is a need to input x-access-token header for some routes (covered in the guide later).

-----------------------------------------------------------------------------------------------------------------------------------------------------

How to interact with the api:

-----------------------------------------------------------------------------------------------------------------------------------------------------

<b>Create User</b>:
Description-> Register a new user in the system
Route to request (for POSTMAN/Frontend)-> http://127.0.0.1:5000/user
Type of request->POST

Input
{
    "email": STRING,
    "first_name": STRING,
    "last_name": STRING,
    "password": STRING,
    "contact_number": INT
}

Example Input
{
    "email": "aaron@gmail.com",
    "first_name": "Aaron",
    "last_name": "Tan",
    "password": "password"
    "contact_number": 99911122
}


Success Output
{
    "message": "Congrats Aaron! Your account has been created."
}

Fail Output
{
    "message": "Account creation failed."
}


-----------------------------------------------------------------------------------------------------------------------------------------------------

<b>User Login:</b>
Description-> Login username/email and password. A uniquely generated public_id and JWT Token will return upon successful login. Token is only available for 60min. Public_ID will be used in place of email to access user's detail route so that the frontend don't need to pass in email (sensitive data) to backend for processing.
Route to request (for POSTMAN/Frontend)-> http://127.0.0.1:5000/login
Type of request->GET, Basic Authorization(in Postman app)

Input
Username: <YOUR EMAIL>
Password: <YOUR PASSWORD>

Example Input
Username: aaron@gmail.com
Password: password

Success Output
{
    "public_id": "e8e1f418-1100-41be-b823-36bc6ad34da1",
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiJlOGUxZjQxOC0xMTAwLTQxYmUtYjgyMy0zNmJjNmFkMzRkYTEiLCJleHAiOjE2NDY3OTUzNTl9.OmAmuNAEihwkbLK9w0SIBuXoodbbgsjcoe0iDm_wNC8"
}

Fail Output
Username/Email does not exist, please try again

-----------------------------------------------------------------------------------------------------------------------------------------------------

<b>Query user's detail:</b>
Description-> Get current user's detail, only user with authorized token is able to query this data, or else blocked.

Route to request (for POSTMAN/Frontend)-> http://127.0.0.1:5000/user/<PUBLIC_ID>
Type of request->GET
Header needed:
Key: x-access-token
Value:<TOKEN>

Input (header)
Key: x-access-token
Value:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiI2NmQ0Yjg5OS05YTZiLTRlZWItOTM2YS0wMmM2MWEzOGJiM2IiLCJleHAiOjE2NDY3MjA0NTJ9.GiibULsXooDCmV6vcnZ6LlbVJSjb-RYrOe58wvjzy3g


Input Route
http://127.0.0.1:5000/user/e8e1f418-1100-41be-b823-36bc6ad34da1


Success Output
{
    "data": {
        "contact_number": 99911122,
        "email": "aaron@gmail.com",
        "first_name": "Aaron",
        "last_name": "Tan",
        "password": "sha256$J95CMggsCAGiUEGn$59a7b8c4202e95cb766a71efc97b5315baf958ef44bf0ca68c75f8569d41de06",
        "public_id": "e8e1f418-1100-41be-b823-36bc6ad34da1"
    },
    "message": "User's details have been retrieved successfully"
}

Fail Output
{
    "message": "Token is invalid!"
}

-----------------------------------------------------------------------------------------------------------------------------------------------------

<b>Get Carpark Availability:</b>
Description-> Get carpark availability from an API, only user with authorized token is able to query this data, or else blocked.
Route to request (for POSTMAN/Frontend)-> http://127.0.0.1:5000/car
Type of request->GET
Header needed:
Key: x-access-token
Value:<TOKEN>

Input (header)
Key: x-access-token
Value:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiI2NmQ0Yjg5OS05YTZiLTRlZWItOTM2YS0wMmM2MWEzOGJiM2IiLCJleHAiOjE2NDY3MjA0NTJ9.GiibULsXooDCmV6vcnZ6LlbVJSjb-RYrOe58wvjzy3g


Success Output
{
    "data": {
        "items": [
            {
                "carpark_data": [
                    {
                        "carpark_info": [
                            {
                                "lot_type": "C",
                                "lots_available": "0",
                                "total_lots": "105"
                            }
                        ],
.
.
.


Fail Output
{
    "message": "Token is invalid!"
}

-----------------------------------------------------------------------------------------------------------------------------------------------------