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
    weather=data.get("mars_weather")
    the_news_link= data.get("news_link")[0]
    the_news_title= data.get("news_title")[0]
    the_news_teaser=data.get("news_teaser")[0]
    image_title_list=data.get("image_title_list")
    image_url_list=data.get("image_url_list")

    return render_template("test.html", this_table=this_table, 
        image_url=image_url, 
        mars_weather=weather,
        the_news_link=the_news_link,
        the_news_title=the_news_title,
        the_news_teaser=the_news_teaser,
        image_title_list=image_title_list,
        image_url_list=image_url_list)


if __name__ == "__main__":
    app.run(debug=True)