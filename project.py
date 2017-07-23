#Web app made on Flask
#Author: Ankit Raj Ojha


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

from flask import Flask, render_template, request,redirect,url_for,flash,jsonify,session
import os
from userdatabase import*



app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
Session = DBSession()
# JSON
@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = Session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = Session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    menuItem = Session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(menuItem.serialize)

#Restaurant page when logged in

@app.route('/')
@app.route('/restaurant')
def restaurant():
    restaurant= Session.query(Restaurant).all()
    return render_template('restaurant.html', restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/')
def restaurantmenu(restaurant_id):
    restaurant=Session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = Session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html',restaurant=restaurant,items=items)


@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET','POST'])
def editRestaurant(restaurant_id):
    editedRestaurant=Session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method=='POST':
        if request.form['name']:
            editedRestaurant=request.form['name']
        Session.add(editedRestaurant)
        Session.commit()
        return redirect(url_for('restaurant', restaurant_id=restaurant_id))
    else:
        return render_template('editRestaurant.html', restaurant_id=restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET','POST'])
def deleteRestaurant(restaurant_id):
    deletedRestaurant=Session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method=='POST':
        Session.delete(deletedRestaurant)
        Session.commit()
        return redirect(url_for('restaurant', restaurant_id=restaurant_id))
    else:
        return render_template('deleteRestaurant.html', restaurant_id=restaurant_id)
@app.route('/restaurant/new', methods=['GET','POST'])
def newRestaurant():
    if request.method=='POST':
        newName=Restaurant(name=request.form['name'])
        Session.add(newName)
        Session.commit()
        flash('New restaurant added')
        return redirect(url_for('restaurant'))
    else:
        return render_template('newRestaurant.html')

#Restaurant Page when not logged in
@app.route('/mainrestaurant')
def mainRestaurant():
    restaurant= Session.query(Restaurant).all()
    return render_template('mainRestaurant.html', restaurant=restaurant)

@app.route('/mainrestaurant/<int:restaurant_id>/')
def mainRestaurantmenu(restaurant_id):
    restaurant=Session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = Session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('mainmenu.html',restaurant=restaurant,items=items)

@app.route('/restaurant/<int:restaurant_id>/orders')
def orderMenu(restaurant_id,menu_id):
    return "for orders"



# Menu page
@app.route('/restaurant/<int:restaurant_id>/new', methods=['GET','POST'])
def newMenuItem(restaurant_id):
    if request.method=='POST':
        newItem=MenuItem(name = request.form['name'], price=request.form['price'], description=request.form['description'], restaurant_id=restaurant_id)
        Session.add(newItem)
        Session.commit()
        flash("New menu added")
        return redirect(url_for('restaurantmenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit', methods=['GET','POST'])
def editMenuItem(restaurant_id,menu_id):
    editedItem = Session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name=request.form['name']
        Session.add(editedItem)
        Session.commit()
        return redirect(url_for('restaurantmenu', restaurant_id=restaurant_id))
    else:
        return render_template('editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, i= editedItem)

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete', methods=['GET','POST'])
def deleteMenuItem(restaurant_id,menu_id):
    deleteditem = Session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method=='POST':

        Session.delete(deleteditem)
        Session.commit()
        return redirect(url_for('restaurantmenu', restaurant_id=restaurant_id))
    else:
        return render_template('deletemenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, i=deleteditem)

# Login page
engine = create_engine('sqlite:///userdata.db', echo=True)


@app.route('/home')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return restaurant()


@app.route('/login', methods=['POST'])
def do_admin_login():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])

    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]))
    result = query.first()
    if result:
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()


if __name__=='__main__':
    app.secret_key=os.urandom(10)
    app.debug = True
    app.run(host='0.0.0.0',port=5000)


#Source : Udacity