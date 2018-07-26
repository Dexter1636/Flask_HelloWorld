from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurant_menu.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)


class Restaurant(db.Model):
    __tablename__ = 'restaurant'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250), nullable=False)


class MenuItem(db.Model):
    __tablename__ = 'menu_item'

    name = db.Column(db.String(80), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(250))
    price = db.Column(db.String(8))
    course = db.Column(db.String(250))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    restaurant = db.relationship(Restaurant)





@app.route('/print', methods=['GET', 'POST'])
def print_str():
    if request.method == 'GET':
        return render_template('print_get.html')
    if request.method == 'POST':
        str = request.form['str']
        return render_template('print_post.html', str=str)


@app.route('/')
@app.route('/index')
@app.route('/restaurant')
def index():
    restaurants = db.session.query(Restaurant).all()
    return render_template('index.html', restaurants=restaurants)


@app.route('/restaurant/new', methods=['GET', 'POST'])
def new_restaurant():
    if request.method == 'GET':
        return render_template('new_restaurant.html')
    if request.method == 'POST':
        new_restaurant = Restaurant(name=request.form['name'])
        db.session.add(new_restaurant)
        db.session.commit()
        flash("new restaurant " + request.form['name'] + " created!")
        return redirect(url_for('index'))


@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def edit_restaurant(restaurant_id):
    if request.method == 'GET':
        restaurant = db.session.query(Restaurant).filter_by(id=restaurant_id).one()
        restaurant_name = restaurant.name
        return render_template('edit_restaurant.html', restaurant_id=restaurant_id, restaurant_name=restaurant_name)
    if request.method == 'POST':
        restaurant = db.session.query(Restaurant).filter_by(id=restaurant_id).one()
        restaurant.name = request.form['name']
        db.session.add(restaurant)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/restaurant/<int:restaurant_id>/delete')
def delete_restaurant(restaurant_id):
    restaurant = db.session.query(Restaurant).filter_by(id=restaurant_id).one()
    db.session.delete(restaurant)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/restaurant/<int:restaurant_id>/new_menu_item')
def new_menu_item(restaurant_id):
    return "page to create a new menu item. Task 1 complete!"


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit_menu_item')
def edit_menu_item(restaurant_id, menu_id):
    return


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete_menu_item')
def delete_menu_item(restaurant_id, menu_id):
    return


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
