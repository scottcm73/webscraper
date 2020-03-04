import selenium
from bs4 import BeautifulSoup
import pandas as pd
import requests
import pymongo 
import json



class Scraper():
    URL_list = ["https://mars.nasa.gov/news/", 
            "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars",
            "https://twitter.com/marswxreport?lang=en",
            "http://space-facts.com/mars/",
            "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"]
    
    
    def __init__(self):
        URL_list=Scraper.URL_list
        return
    def scrape(self, URL):
  
            
        html = requests.get(URL).text
        soup = BeautifulSoup(html, "html.parser")
        self.soup=soup
        return self.soup

    
    def xml_scrape(self, URL):
        html = requests.get(URL).text
        soup = BeautifulSoup(html, "lxml")
        self.soup=soup
        return self.soup

   


    def local_file_scrape(self, FILE):
        self.FILE=FILE 
        soup = BeautifulSoup(open(FILE, encoding='utf8'), "lxml")

        self.soup=soup
        return self.soup


    def find_content(self): 
        # Mars news scrape
        URL_list=Scraper.URL_list
        soup=self.scrape(URL_list[0])
        self.URL_list = URL_list
        news_link_list=[] 
        news_title_list=[]
        news_teaser_list=[]
 
        for data in soup.find_all('div', class_='content_title'):
            for a in data.find_all('a'):
                news_title=a.text
                news_title=news_title.replace('\n', '')
                news_link=URL_list[0] + a.get('href')
                news_link_list.append(news_link)
                news_title_list.append(news_title) #for getting text between the link and the close anchor tag
                self.news_link_list=news_link_list
                self.news_title_list=news_title_list
                # Crawls to news_link page from original page
                soup2=self.scrape(news_link)

                for data in soup2.find_all('div', class_='wysiwyg_content'):
                    p=data.find('p')
                    article_text=p.text
                    article_text=article_text.replace("\\", "")
                    news_teaser_list.append(article_text)
                    self.news_teaser_list=news_teaser_list
        
        #Finds url of full image from button link
        soup=self.scrape(URL_list[1])
        for a in soup.find_all("a", class_="button fancybox"):
            featured_image_url = a.get("data-fancybox-href")
            featured_image_url = "https://www.jpl.nasa.gov/" + featured_image_url
            self.featured_image_url=featured_image_url

        # Mars weather scrape

        soup2 = self.scrape(URL_list[2])
        mars_weather=soup2.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
        mars_weather_text=mars_weather.text

        #I had to take out the pic from the text...
        sep="pic"
        mars_weather = mars_weather_text.split(sep, 1)[0]

        self.mars_weather=mars_weather

        # Mars facts scrape
        

        soup2 = self.scrape(URL_list[3])
        FILE = "html_mars_facts.html"
        with open(FILE, "w+", encoding="utf-8") as f:
            f.write(soup2.prettify())

        soup=BeautifulSoup((open(FILE)), 'lxml')     
        table = soup.find_all('table')[0] 
        df = pd.read_html(str(table))[0]

        df.columns=['Fact', 'Info']

        
        df.reset_index(None)
   
        df_html=df.to_html() 

       

        print(df_html)
       
      
        
        df_html=df_html.replace("\n", "")
       
        self.df_html=df_html
       

        #Astrogeology scrape
        title_list=[]
        image_url_list=[]

        soup2 = self.scrape(URL_list[4])

       
        FILE = "html_astrogeology_scrape.html"
        with open(FILE, "w+", encoding="utf-8") as f:
            f.write(soup2.prettify())

        soup=BeautifulSoup((open(FILE)), 'lxml') 
        for a in soup.find_all('a', class_='itemLink product-item'):
            title=a.text
            title=title.replace("\n", "")
            title_list.append(title)
            link_url=a.get("href")
            link_url="https://astrogeology.usgs.gov" + link_url

            #Crawls to this new page to scrape data

            soup3=self.scrape(link_url)

            FILE = "html_astrogeology_scrape2.html"
            #Makes new file locally
            with open(FILE, "w+", encoding="utf-8") as f:
                f.write(soup3.prettify())
            
            soup4=BeautifulSoup((open(FILE)), 'lxml') 
            #Navigate to new page to get better image
            a = soup4.find('a', target='_blank')
            image_link=a.get("href")
            image_url_list.append(image_link)
    
        image_dict={"image_url": image_url_list, "title": title_list}
        self.image_dict=image_dict
        self.image_url_list=image_url_list
        self.image_title_list=title_list
        print(self.image_title_list)
        print(self.image_url_list)
    def to_json(self):
        this_dict={"_id":"mars", "news_link": self.news_link_list, 
                    "news_title": self.news_title_list, 
                    "news_teaser": self.news_teaser_list,
                    "featured_image_url" :self.featured_image_url,
                    "mars_weather":self.mars_weather,
                    "facts_table":self.df_html,
                    "image_dict":self.image_dict,
                    "image_title_list":self.image_title_list,
                    "image_url_list":self.image_url_list
                    }


        

                   
        self.this_dict=this_dict
        return 
    
    def to_mongo(self):
        news_list=[]

        client = pymongo.MongoClient('localhost', 27017)
        self.client=client
        db_list=client.list_database_names()
        if 'mars_scrape_db' in db_list:
            client.drop_database('mars_scrape_db')
        db = client['mars_scrape_db']
        
        
        

       
        collection_mars_scrape = db['mars_scrape']
    
        self.collection_mars_scrape=collection_mars_scrape

        collection_mars_scrape.insert_one(self.this_dict)

        
    def from_mongo(self):
        client = pymongo.MongoClient('localhost', 27017)
        db = client['mars_scrape_db']
        data=db.mars_scrape.find_one({})
        self.data=data
        return        

        

       

        
      
      

    def get_data(self):
        
        data=self.data
       
        return
       

    
        


        