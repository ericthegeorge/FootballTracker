# FootballTracker

A project by Eric George, Roko Condic, and Bassel Hasan. It will track professional football teams and players and they're data, presenting them in a fun and fan-oriented manner.

# Setup

## Installing Django

Assuming you have python installed, which is the base language for Django, you can run the following commands in terminal:

`pip install django`
`pip install djangorestframework`
`pip install mysqlclient`
`pip install python-dotenv`

Next, open your MySQL workbench. If you don't have it installed already, you can install it [here](https://dev.mysql.com/downloads/mysql/).

## Creating Your Database
If this is you're first time with MySQL, you'll need to create a local instance connection that you'll work on. The names here don't really matter, the databases are 'schemas' here. You can create it with the default settings, with any name you wish (Local Instance, loc, ROKOROKOROKOandapinchofBassel). It should look something like this in setup:
![image](https://github.com/user-attachments/assets/3e2038ff-10dd-4e26-abb6-d2a6953d99c4)

Once you're in, create the schema for our FootballTracker database. Right-click in the schema's section to select the 'Create Schema' option, and give it a name with the default options.
![image](https://github.com/user-attachments/assets/587a1ccc-38d3-4b3e-be6f-d313ca72fe66)

## Adding Your Environment Variables
Once this is done, you'll want to head back over to our code in your IDE. Create your own .env file (explicity just '.env') in the Backend folder, beside manage.py and the footballtracker folder. This is personal information, so it's added to the gitignore and will not be committed into the repository. Add your details here like so:

`
DB_NAME= THE_name_WOW
DB_USER=root
DB_PASSWORD=perhapsthereisapasswordhereperhaps
DB_HOST= 127.0.0.1
DB_PORT= 3306
`

This allows each of us to maintain our local instance of the database, without interfering with each other's configurations. Since we're only deploying locally for a test, this is the easiest way to go for now. We can consider database sharing later, as it isn't relevant to development right now. If need be for some test data, we can send the csv's (or other file formats) to share the data.

![image](https://github.com/user-attachments/assets/bb6a5502-13c7-423f-af78-2146c2179301)
