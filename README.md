# Restaurant_menu

First you need to install things-

1. SQLAlchemy 
   ```pip install SQLAlchemy```

2. Flask
   ```pip install flask```

## Run the flask version code-

1. Run ```database_setup.py```.This will create a database called restaurantmenu.db .
2. Run ```lotsofmenus.py```. This will add menus in the database.
3. Run ```userdatabase.py``` to create a database for the user userdata.db .
4. Run ```loginuser.py``` to add the users in the userdatbase.
5. Run ```project.py``` to run the project in the localhost.

After Running all the above commands, in your web browser open ```localhost:5000/mainrestaurant```. This will the Main Restaurant page for the non owner's. After logging in you can add/edit/delete Restaurants and menus. Password for the login is right there in files find it( they are not hashed). For security purpose it should be hashed.

## Run the old version-

( Its not completed )
1. Run ```database_setup.py```.This will create a database called restaurantmenu.db .
2. Run ```lotsofmenus.py```. This will add menus in the database.
3. Run ```webserver.py``` to run the project in the localhost.


##
Project created with flask framework is much better than the project created in old ways. Not only it reduces the length of code but also give lots addition features over the olden version and also it is easy develop the project in flask framework than the olden way.
