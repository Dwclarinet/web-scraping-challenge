from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of our Flask app.
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Create connection variable
#conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
#client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
#db = client.mars_db

# Drops collection if available to remove duplicates
#db.mars_info.drop()

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_data = mongo.db.mars_info.find_one()

    # Return template and data
    return render_template("index.html", mars_data=mars_data)

# Set route
@app.route('/scrape')
def mars_scrape():
    mars_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.mars_info.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("http://localhost:5000/")

if __name__ == "__main__":
    app.run(debug=True)