#Web app made on Flask
#Author: Ankit Raj Ojha


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

from flask import Flask, render_template, request,redirect,url_for,flash,jsonify
app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
# JSON
@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(menuItem.serialize)

#Restaurant page

@app.route('/')
@app.route('/restaurant')
def restaurant():
    restaurant= session.query(Restaurant).all()
    return render_template('restaurant.html', restaurant=restaurant)

@app.route('/restaurant/<int:restaurant_id>/')
def restaurantmenu(restaurant_id):
    restaurant=session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html',restaurant=restaurant,items=items)


@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET','POST'])
def editRestaurant(restaurant_id):
    editedRestaurant=session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method=='POST':
        if request.form['name']:
            editedRestaurant=request.form['name']
        session.add(editedRestaurant)
        session.commit()
        return redirect(url_for('restaurant', restaurant_id=restaurant_id))
    else:
        return render_template('editRestaurant.html', restaurant_id=restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET','POST'])
def deleteRestaurant(restaurant_id):
    deletedRestaurant=session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method=='POST':
        session.delete(deletedRestaurant)
        session.commit()
        return redirect(url_for('restaurant', restaurant_id=restaurant_id))
    else:
        return render_template('deleteRestaurant.html', restaurant_id=restaurant_id)
@app.route('/restaurant/new', methods=['GET','POST'])
def newRestaurant():
    if request.method=='POST':
        newName=Restaurant(name=request.form['name'])
        session.add(newName)
        session.commit()
        flash('New restaurant added')
        return redirect(url_for('restaurant'))
    else:
        return render_template('newRestaurant.html')



# Menu page
@app.route('/restaurant/<int:restaurant_id>/new', methods=['GET','POST'])
def newMenuItem(restaurant_id):
    if request.method=='POST':
        newItem=MenuItem(name = request.form['name'], price=request.form['price'], description=request.form['description'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("New menu added")
        return redirect(url_for('restaurantmenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit', methods=['GET','POST'])
def editMenuItem(restaurant_id,menu_id):
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name=request.form['name']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('restaurantmenu', restaurant_id=restaurant_id))
    else:
        return render_template('editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, i= editedItem)

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete', methods=['GET','POST'])
def deleteMenuItem(restaurant_id,menu_id):
    deleteditem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method=='POST':

        session.delete(deleteditem)
        session.commit()
        return redirect(url_for('restaurantmenu', restaurant_id=restaurant_id))
    else:
        return render_template('deletemenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, i=deleteditem)




if __name__=='__main__':
    app.secret_key='super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0',port=5000)


#Source : Udacity