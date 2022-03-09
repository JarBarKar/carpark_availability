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

<b>Create User</b>:<br>
Description-> Register a new user in the system<br>
Route to request (for POSTMAN/Frontend)-> http://127.0.0.1:5000/user<br>
Type of request->POST<br>

Input<br>
{
    "email": STRING,
    "first_name": STRING,
    "last_name": STRING,
    "password": STRING,
    "contact_number": INT
}<br><br>

Example Input<br>
{
    "email": "aaron@gmail.com",
    "first_name": "Aaron",
    "last_name": "Tan",
    "password": "password"
    "contact_number": 99911122
}<br><br>


Success Output<br>
{
    "message": "Congrats Aaron! Your account has been created."
}
<br>
Fail Output<br>
{
    "message": "Account creation failed."
}


-----------------------------------------------------------------------------------------------------------------------------------------------------

<b>User Login:</b><br>
Description-> Login username/email and password. A uniquely generated public_id and JWT Token will return upon successful login. Token is only available for 60min. Public_ID will be used in place of email to access user's detail route so that the frontend don't need to pass in email (sensitive data) to backend for processing.<br>
Route to request (for POSTMAN/Frontend)-> http://127.0.0.1:5000/login<br>
Type of request->GET, Basic Authorization(in Postman app)<br>

Input<br>
Username: <YOUR EMAIL><br>
Password: <YOUR PASSWORD><br>

Example Input<br>
Username: aaron@gmail.com<br>
Password: password<br>

Success Output<br>
{
    "public_id": "e8e1f418-1100-41be-b823-36bc6ad34da1",
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiJlOGUxZjQxOC0xMTAwLTQxYmUtYjgyMy0zNmJjNmFkMzRkYTEiLCJleHAiOjE2NDY3OTUzNTl9.OmAmuNAEihwkbLK9w0SIBuXoodbbgsjcoe0iDm_wNC8"
}
<br>
Fail Output<br>
Username/Email does not exist, please try again<br>

-----------------------------------------------------------------------------------------------------------------------------------------------------

<b>Query user's detail:</b><br>
Description-> Get current user's detail, only user with authorized token is able to query this data, or else blocked. Do note to insert the retrieved PUBLIC_ID from login request and replace it at the route below.<br>

Route to request (for POSTMAN/Frontend)-> http://127.0.0.1:5000/user/<PUBLIC_ID><br>
Type of request->GET<br>
Header needed:<br>
Key: x-access-token<br>
Value:-TOKEN-<br>

Input (header)<br>
Key: x-access-token<br>
Value:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiI2NmQ0Yjg5OS05YTZiLTRlZWItOTM2YS0wMmM2MWEzOGJiM2IiLCJleHAiOjE2NDY3MjA0NTJ9.GiibULsXooDCmV6vcnZ6LlbVJSjb-RYrOe58wvjzy3g<br>

Success Output<br>
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
}<br><br>

Fail Output<br>
{
    "message": "Token is invalid!"
}

-----------------------------------------------------------------------------------------------------------------------------------------------------

<b>Get Carpark Availability:</b><br>
Description-> Get carpark availability from an API, only user with authorized token is able to query this data, or else blocked.
Route to request (for POSTMAN/Frontend)-> http://127.0.0.1:5000/car<br>
Type of request->GET<br>
Header needed:<br>
Key: x-access-token<br>
Value:-TOKEN-<br>

Input (header)<br>
Key: x-access-token<br>
Value:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiI2NmQ0Yjg5OS05YTZiLTRlZWItOTM2YS0wMmM2MWEzOGJiM2IiLCJleHAiOjE2NDY3MjA0NTJ9.GiibULsXooDCmV6vcnZ6LlbVJSjb-RYrOe58wvjzy3g<br>


Success Output<br>
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


Fail Output<br>
{
    "message": "Token is invalid!"
}

-----------------------------------------------------------------------------------------------------------------------------------------------------

<b>*Note that the inputted values are placeholder, such as token value and public ID
