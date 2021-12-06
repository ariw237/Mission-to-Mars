#Use Flask  and Mongo to create a webapp
#Import dependencies
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping #scraping.py should be in same directory

#Setup flask
app = Flask(__name__)
#Import to create mongodb called "mars_app"
#Use flask_pymongo to set up mongo connection using a uniform resource identifier and port 27017
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)
#Define a route to our html page
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template('index.html', mars=mars)


#Setup our scraping route which includes a scraping button

@app.route("/scrape")  #Defines our route
def scrape():
    mars = mongo.db.mars     #Assign variable to point to database
    mars_data = scraping.scrape_all()     #Assign variable to results of scraping
    #Create an empty json object that contains mars_data:
    mars.update({}, mars_data, upsert=True) #Update our database
    return redirect('/', code=302)  #Navigate page back to root

if __name__ == "__main__":
    app.run()
