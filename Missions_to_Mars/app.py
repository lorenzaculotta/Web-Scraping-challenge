from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

#def pymongo connection
conn="mongodb://localhost:27017"

#Create a root route / that will query your Mongo database and pass the mars 
# data into an HTML template to display the data.

@app.route("/")
def index():
    #pass connection
    client=pymongo.MongoClient(conn)

    # Define database and collection
    db= client.mars_db
    collection= db.hemispheres

    #store mars_dictionary collection
    mars_dict =collection.find_one()
    print(mars_dict)
 
    return render_template("index.html",  mars_dict= mars_dict)




# create a route called /scrape that will import your scrape_mars.py script and call your scrape function.
@app.route("/scrape")
def scrape():
    #pass connection
    client=pymongo.MongoClient(conn)

    # Define database and collection
    db= client.mars_db
    collection= db.hemispheres

    #retrieved dictionaries
    mars_dict=scrape_mars.scrape()
    print(mars_dict)

    #Store the return value in Mongo as a Python dictionary
    # collection.insert_many(hemisphere_image_urls)
    collection.update({}, mars_dict, upsert=True)

    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
    