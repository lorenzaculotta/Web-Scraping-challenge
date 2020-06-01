from flask import Flask, render_template, redirect
import pymongo
# from flask_pymongo import PyMongo
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

    # #store all variables to be passed to the HTML template
    # news_title = mars_dict["news_title"]
    # news_p = mars_dict["news_p"]
    # featured_image_url = mars_dict["featured_image_url"]
    # mars_html = mars_dict["mars_html"]
    # hemisphere_dict = mars_dict["hemisphere_dict"]
    
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
    


    # player_dictionary = {"player_1": "Jessica",
    #                      "player_2": "Mark"}
    # return render_template("index.html", dict=player_dictionary)




if __name__ == "__main__":
    app.run(debug=True)