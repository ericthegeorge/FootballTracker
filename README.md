# FootballTracker

A project by Eric George, Roko Condic, and Bassel Hasan. It will track professional football teams and players and they're data, presenting them in a fun and fan-oriented manner.

# Information

Frontend: Flutter (with dart, targeted for web deployment)
Backend: Django
Database: MySQL local
RESTful API

Please add your design boards, drafts, or other ideas you have here.

All work should be committed to specific branches, and merged onto main. BE WARY OF MERGE CONFLICTS. Don't accept merges easily and overwrite another person's work. Ideally someone should review all pull requests, but this will not be enforced.

# Setup

## Installing Django

Assuming you have python installed, which is the base language for Django, you can run the following commands in terminal:

`pip install django`
`pip install djangorestframework`
`pip install mysqlclient`
`pip install python-dotenv`
`pip install Pillow`

Next, open your MySQL workbench. If you don't have it installed already, you can install it [here](https://dev.mysql.com/downloads/mysql/).

### Creating Your Database

If this is you're first time with MySQL, you'll need to create a local instance connection that you'll work on. The names here don't really matter, the databases are 'schemas' here. You can create it with the default settings, with any name you wish (Local Instance, loc, ROKOROKOROKOandapinchofBassel). It should look something like this in setup:
![image](https://github.com/user-attachments/assets/3e2038ff-10dd-4e26-abb6-d2a6953d99c4)

Once you're in, create the schema for our FootballTracker database. Right-click in the schema's section to select the 'Create Schema' option, and give it a name with the default options.
![image](https://github.com/user-attachments/assets/587a1ccc-38d3-4b3e-be6f-d313ca72fe66)

### Adding Your Environment Variables

Once this is done, you'll want to head back over to our code in your IDE. Create your own .env file (explicity just '.env') in the Backend folder, beside manage.py and the footballtracker folder.
![image](https://github.com/user-attachments/assets/bb6a5502-13c7-423f-af78-2146c2179301)

This is personal information, so it's added to the gitignore and will not be committed into the repository. Add your details here like so:

`
DB_NAME= THE_name_WOW`
`DB_USER=root`
`DB_PASSWORD=perhapsthereisapasswordhereperhaps`
`DB_HOST= 127.0.0.1`
`DB_PORT= 3306
`

This allows each of us to maintain our local instance of the database, without interfering with each other's configurations. Since we're only deploying locally for a test, this is the easiest way to go for now. We can consider database sharing later, as it isn't relevant to development right now. If need be for some test data, we can send the csv's (or other file formats) to share the data.

Finally, you're going to run the following commands in your terminal (in the root folder of "FootballTracker/Backend"):

`python manage.py makemigrations`
`python manage.py migrate`

This will setup Django's authentication models in our schema.

### Further Information on Django

Most of the backend functionality for local deployment will come from running some arguments on manage.py. The manage.py file is what calls the code, and we do actions by giving it the proper args (in command line), like makemigrations or runserver. Below are some important Django commands.

`python manage.py runserver`

Starts a lightweight development web server on the local machine. By default, the server runs on the IP address 127.0.0.1. You can pass in an IP address and port number explicitly. Use this when you want to test (locally).

`python manage.py makemigrations`

Creates new migrations based on the changes detected to your models. Migrations, their relationship with apps and more are covered in depth in the migrations documentation in the link below. Models are essentially tables from our database. We interact with them through the Models we create in Django.

`python manage.py migrate`

Synchronizes the database state with the current set of models and migrations. Migrations, their relationship with apps and more are covered in depth in the migrations documentation in the link below.

[Django/Python documentation](https://docs.djangoproject.com/en/5.1/ref/django-admin/) (the commands differ, but generally use the name as the cmd line argument for manage.py).

## Installing Flutter

The first thing you'll need to do is install Flutter and it's SDK in your device and IDE of choice. You can do this by following the instructions [here](https://docs.flutter.dev/get-started/install/windows/web) (this is the web-app configuration of flutter installation).

Note: If adding it to your path environment doesn't apply properly, try using the absolute path instead of the %USERPROFILE%
based one.

At this point, you may need to close and reopen your IDE for it to reload your terminal (and thereby recognize flutter commands). You can check if Flutter is recognized with a simple version commmand:
`flutter doctor --version`

If it works, you're all ready for development!

### Further Information on Flutter

You can find general documentation for Flutter at: https://docs.flutter.dev/ \
Detailed API documentation is available at: https://api.flutter.dev/ \
If you prefer video documentation, consider: https://www.youtube.com/c/flutterdev

# Development 🙌

## Database Development

Most of the database development you'll be doing is in the Django code. Specifically, Backend/footballtracker/models.py (and a little bit in admin.py). Take a look at the docs and api to understand the structure. I also added an example with a primary key and a foreign key to help.

## Backend Development

There's a few key files here where you'll devote most of your time. In Backend: views.py, serializers.py; and in footballtracker: urls.py and settings.py. We're using a REST framework, which basically means our frontend calls a link with some info, and we put our response on that link. We setup the urls to call in urls, the data parsing is in serializers (for sending and receiving JSON's), and the views.py is where the logic of the response is. Settings is for anything you might change, as I'm sure you may find things are insufficient. I'll add an example across these to show what it could look like. The example is with user registration, although please note you cannot use this implementation example, and you'll probably need to design a different scheme where we actually use proper security instead of having the password in the payload of the https request.

## Frontend Development

Frontend probably looks the most confusing, but fear not! If you wanted to (although I would be greatly aggrieved if you did), you could do all your frontend work in one file! This important file is your main.dart (specifically, frontend/lib/main.dart). The code will run main, which creates your Flutter App struct, called MyApp. It's a stateless widget altogther, although you can have states within or even alter it's stateless nature. You may also create some files to add your App's structure. As well, an api_service could be helpful in managing the backend rest framework which you will use for backend interactions. I'll provide an example api service, although it may not be effective for our backend.

For adding dependencies (imports and the like), you'll need to add them under dev_dependencies in the pubspec.yaml file. This file should be in the root of frontend.
Flutter commands to build and clean:

`flutter clean`
`flutter pub get`

Command to update your flutter and it's SDK:

`flutter upgrade`

Command to 'doctor' your flutter issues:

`flutter doctor`

# Testing

Testing here is pretty simple. Once you've saved all your changes - made migrations and migrated it in Django, and saved all your code - then open up two command line terminals (you can do this within your IDE, it should work fine). In the first one, cd into Backend, and run 
`python manage.py runserver`

This starts up the backend server (locally) so the frontend can start making requests.

To start up your flutter app, just run
`flutter run`

It'll prompt you for which device you want to deploy to, just enter the number associated to web or desktop (web might be faster to build and it's also what we'll present). Then you should see your flutter app, and any interaction with the backend should be successful (provided, your code is not bugged). 

Happy testing! 😁

# Other Notes

We should update this readme if anyone finds issues with setup or development, or finds anything else to contribute. It's important we do this so the information is shared and we can work efficiently. It's like commenting but 10x better (worse). But it's important 😭.

If you're ever stuck, you can refer to some example code (that is, my Cardfight Vanguard project on github) that shares similar structure (I wonder why 💯). It can help give you some direction, although I will say the structure is very inefficient and improper there, so consult the official development guidelines, API, and other online resources as well.

Also, make sure you are pulling before you work and commit, it's important you work on the most up to date code.

Hopefully the setup goes smoothly for everyone. Development is the fun part so let's enjoy it! 🙌
