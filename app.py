from flask import Flask, render_template
from scrape_mars import Scraper
import lxml
import pymongo 

app = Flask(__name__)
this_scraper=Scraper()

this_scraper.find_content()
this_scraper.to_json()
this_scraper.to_mongo()
this_scraper.get_data()

@app.route("/")
def home():
    mars_dict=this_scraper.data
    

    
    return render_template("test.html", mars_dict=mars_dict)
@app.route("/json")
def json():
    client = pymongo.MongoClient('localhost', 27017)
    db = client['mars_scrape_db']
    collection_mars_scrape = db['mars_scrape']
    data=db.mars_scrape.find_one({})
    this_table=data.get("facts_table") 
    image_url=data.get("featured_image_url")
    return render_template("test.html", this_table=this_table, image_url=image_url)

if __name__ == "__main__":
    app.run(debug=True)