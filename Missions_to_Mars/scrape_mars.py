#Dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser

def scrape():
    ## 1) NASA Mars News
    ##Web scraping with BeautifulSoup

    # URL of page to be scraped
    url="https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

    # Retrieve page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object
    soup = bs(response.text, 'html.parser')

    # Examine the results, then determine element that contains sought info
    # print(soup.prettify())

    # results are returned as an iterable list
    results = soup.find_all("div", class_="slide")
    # results

    news_title = results[0].find("div", class_="content_title").text
    news_p= results[0].find("div", class_="rollover_description_inner").text
    if (news_title and news_p ):
        print(news_title)
        print(news_p)

    #------------------------------------------------------------------------
    ## 2) JPL Mars Space Images - Featured Image
    ##Web scraping with Splinter and bs
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # HTML object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')
    # print(soup.prettify())

    #find the image url for the current Featured Mars Image
    featured_image= soup.find("article", class_="carousel_item")

    #store url into variable
    featured_image_url= f'https://www.jpl.nasa.gov{featured_image.a["data-fancybox-href"]}'
    # featured_image_url

    browser.quit()

    #-----------------------------------------------------------------------------------------------
    ## 3) Mars Facts
    ##Web scraping with Pandas
    url= "https://space-facts.com/mars/"
    table=pd.read_html(url)

    #store results into df
    mars_df=table[0]
    mars_df

    #set index to columns[0] and rename axes
    mars_df=mars_df.set_index(mars_df.columns[0])
    mars_df=mars_df.rename(columns={1: "value"}).rename_axis("description", axis=0)
    mars_df

    #convert the data to a HTML table string
    mars_html=mars_df.to_html()
    mars_html=mars_html.replace('\n', "")
    mars_html

    #------------------------------------------------------------------------------------
    ## 4) Mars Hemispheres
    ##Web scraping with Splinter and bs
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # HTML object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')
    # print(soup.prettify())

    #retrieve hemispheres
    hemispheres=soup.find_all("div", class_="item")

    #create a list to be populated with hemisphere-specific dictionaries 
    hemisphere_image_urls=[]

    #iterate through hemisphere pages to retrieve title and image_url
    for x in hemispheres:
        try:
            #find and visit link to hemisphere-specific page
            href=x.find("a", class_="itemLink product-item")["href"]
            link= f'https://astrogeology.usgs.gov{href}'
    #         print(link)

            browser.visit(link)

            # HTML object and parse with bs
            html = browser.html
            soup = bs(html, 'html.parser')
        #     print(soup.prettify())

            #retrieve image_url
            image=soup.find_all("li")
            image_url=image[0].a["href"]
            
            #retrieve title
            title=soup.find("h2", class_="title").text
            
            #verification prints
            print("-------------")
            print(image_url)
            print(title)


            dict={
                "title": title,
                "image_url": image_url
            }

            hemisphere_image_urls.append(dict)
        
        except AttributeError as e:
            print(e)

    #create a dict with all scraped data
    mars_dict={
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_html": mars_html,
        "hemisphere_dict": hemisphere_image_urls
    }
    browser.quit()

    return mars_dict


