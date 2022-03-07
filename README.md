# carpark_availability

Setup Steps:

Database setup:
1) Go to terminal and navigate to the current directory (the folder that these files are stored).
2) Type "python" and hit Enter. [ignore the ""]
3) Type "from app import db" and hit Enter. You will see a new db file initated in your directory. [ignore the ""]
4) Type "db.create_all()" and hit Enter, so that all the tables will be initated in the DB. [ignore the ""]
5) Type "sqlite3 carpark.db" and hit Enter, to enter SQL mode.
5) Type ".tables" to check that the User table has been created. Once verified, type ".exit" or CTRL-C to exit SQL mode.

Flask setup: