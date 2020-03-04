from flask import Flask, render_template
from scrape_mars import Scraper
import lxml
import pymongo 

app = Flask(__name__)


this_scraper=Scraper()


@app.route("/")
def home():
    this_scraper.from_mongo()
    # Gets data attribute fromt the Scraper class.
    data=this_scraper.data
    this_table=data.get("facts_table") 
    image_url=data.get("featured_image_url")
    weather=data.get("mars_weather")
    the_news_link= data.get("news_link")[0]
    the_news_title= data.get("news_title")[0]
    the_news_teaser=data.get("news_teaser")[0]
    image_titles=data.get("image_title_list")
    image_urls=data.get("image_url_list")
    #Combine the two lists for one iterator
    image_titles_urls=zip(image_titles, image_urls)

    return render_template("test.html", 
        this_table=this_table, 
        image_url=image_url, 
        mars_weather=weather,
        the_news_link=the_news_link,
        the_news_title=the_news_title,
        the_news_teaser=the_news_teaser,
        image_titles_urls=image_titles_urls)
    
@app.route("/scrape")
#Imports Scraper class

def scrape():
    
    this_scraper.find_content()
    this_scraper.to_json()
    this_scraper.to_mongo()
    this_scraper.from_mongo()
    
    # Gets data attribute fromt the Scraper class.
    data=this_scraper.data
    this_table=data.get("facts_table") 
    image_url=data.get("featured_image_url")
    weather=data.get("mars_weather")
    the_news_link= data.get("news_link")[0]
    the_news_title= data.get("news_title")[0]
    the_news_teaser=data.get("news_teaser")[0]
    image_titles=data.get("image_title_list")
    image_urls=data.get("image_url_list")
    #Combine the two lists for one iterator
    image_titles_urls=zip(image_titles, image_urls)

    return render_template("test.html", 
        this_table=this_table, 
        image_url=image_url, 
        mars_weather=weather,
        the_news_link=the_news_link,
        the_news_title=the_news_title,
        the_news_teaser=the_news_teaser,
        image_titles_urls=image_titles_urls)
        

if __name__ == "__main__":
    app.run(debug=True)