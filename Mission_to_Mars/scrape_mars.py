
from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import os
import pandas as pd

def scrape():
    #!which chromedriver
    executable_path={'executable_path':'/usr/local/bin/chromedriver'}
    browser = Browser('chrome',**executable_path, headless=False)

    #Navigate to Mars News website
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    #Find the first article title
    article = soup.find('div', class_='list_text')
    title = article.find('div', class_='content_title')
    news_title = title.find('a').text

    #Find the first article summary
    news_p = article.find('div', class_='article_teaser_body').text

    #Navigate to JPL Image website
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    #Navigate to the full size picture of the day
    browser.click_link_by_partial_text('FULL IMAGE')

    try:
        #If picture isn't full size already, make it full size
        browser.find_by_css('.fancybox-expand').first.click()
    except:
        #Pull out the URL for the picture of the day
        html = browser.html
        soup = bs(html, 'html.parser')
        img_location = soup.find('img', class_='fancybox-image')
        img_url = img_location['src']
        featured_image = f'https://www.jpl.nasa.gov{img_url}'

    #Scrape the picture
    html = browser.html
    soup = bs(html, 'html.parser')
    img_location = soup.find('img', class_='fancybox-image')
    img_url = img_location['src']
    featured_image = f'https://www.jpl.nasa.gov{img_url}'

    #Navigate to Mars Weather Twitter Account
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    #Scrape the latest tweet
    html = browser.html
    soup = bs(html, 'html.parser')
    tweets = soup.find_all('div', class_='js-tweet-text-container')
    for tweet in tweets:
        mars_weather = tweet.find('p').text
        if 'sol' and 'low' and 'high' and 'pressure' in mars_weather:
            break
        else:
            pass

    #Use pandas to scrape mars facts
    url='https://space-facts.com/mars/'
    #browser.visit(url)
    #html = browser.html
    tables = pd.read_html(url)
    marsfact=pd.DataFrame(tables[0])
    marsfact=marsfact.rename(columns={0:'Description', 1:'Value'})
    marsfact=marsfact.set_index('Description')
    mars_facts=marsfact.to_html(classes='table')

    #Create lists
    hemispheres=['Cerberus Hemisphere', 'Schiaparelli Hemisphere', "Syrtis Major Hemisphere", 'Valles Marineris Hemisphere']
    hemisphere_img_urls = []

    #Get Hemisphere Pictures
    for hemisphere in hemispheres:
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)
        browser.click_link_by_partial_text(hemisphere)
        html = browser.html
        soup = bs(html, 'html.parser')
        hemi_page = soup.find('a', text='Sample')
        img_url = hemi_page['href']
        post={
            'title': hemisphere,
            'img_url': img_url
        }
        hemisphere_img_urls.append(post)
        browser.visit(url)

    #Store data in a dictionary
    mars_data={
            'news_title': news_title,
            'news_p': news_p,
            'featured_image': featured_image,
            'mars_weather': mars_weather,
            'mars_facts': mars_facts,
            'hemisphere_img_urls': hemisphere_img_urls
        }

    #Close browser after scraping
    browser.quit()
    
    #Return results
    return mars_data

if __name__ == '__main__':
    scrape()