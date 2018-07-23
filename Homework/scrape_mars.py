
# coding: utf-8

# In[1]:


# Dependencies
import pandas as pd
import re
import requests
import pymongo
from splinter import Browser
from bs4 import BeautifulSoup


# def scrape():In[2]:


# Obtain html of Mars website# Obtai 
mars_news_url = 'https://mars.nasa.gov/news/'
mars_news_html = requests.get(mars_news_url)


# In[3]:


# Parse html file with BeautifulSoup# Parse 
mars_soup = BeautifulSoup(mars_news_html.text, 'html.parser')


# In[4]:


# Print body of html# Print 
print(mars_soup.body.prettify())


# In[7]:


# Find article titles
article_titles = mars_soup.find_all('div', class_='content_title')
article_titles


# In[8]:



# Loop to get article titles# Loop  
for article in article_titles:
    title = article.find('a')
    title_text = title.text
    print(title_text)


# In[11]:



# Find paragraph text# Find  
paragraphs = mars_soup.find_all('div', class_='rollover_description')
paragraphs


# In[13]:



# Loop through paragraph texts# Loop  
for paragraph in paragraphs:
    p_text = paragraph.find('div')
    news_p = p_text.text
    print(news_p)


# In[14]:


# Open browser of Mars space images
mars_images_browser = Browser('chrome', headless=False)
nasa_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
mars_images_browser.visit(nasa_url)


# In[15]:


# Parse html file with BeautifulSoup# Parse  
mars_images_html = mars_images_browser.html
nasa_soup = BeautifulSoup(mars_images_html, 'html.parser')


# In[16]:


# Print body of html
print(nasa_soup.body.prettify())


# In[17]:


# Find image link with BeautifulSoup# Find i 
images = nasa_soup.find_all('div', class_='carousel_items')
images


# In[18]:


# Loop through images
for nasa_image in images:
    image = nasa_image.find('article')
    background_image = image.get('style')
    # print(background_image)
    
    # Use regular expression to extract url - match anything after (.)
    re_background_image = re.search("'(.+?)'", background_image)
    # print(re_background_image)
    
    # Convert match object (url link) to string
    # group(0) includes quotations
    # group(1) gets the url link
    search_background_image = re_background_image.group(1)
    # print(search_background_image)
    
    featured_image_url = f'https://www.jpl.nasa/gov{search_background_image}'
    print(featured_image_url)


# In[19]:


# Get weather tweets with splinter# Get we 
twitter_browser = Browser('chrome', headless=False)
twitter_url = 'https://twitter.com/marswxreport?lang=en'
twitter_browser.visit(twitter_url)


# In[20]:


# Parse html file with BeautifulSoup
twitter_html = twitter_browser.html
twitter_soup = BeautifulSoup(twitter_html, 'html.parser')


# In[21]:


# Print body of html# Print  
print(twitter_soup.body.prettify())


# In[22]:


# Find weather tweets with BeautifulSoup
mars_weather_tweets = twitter_soup.find_all('p', class_='TweetTextSize')
mars_weather_tweets


# In[23]:


# Get tweets that begin with 'Sol' which indicate weather tweets
weather_text = 'Sol '

for tweet in mars_weather_tweets:
    if weather_text in tweet.text:
        mars_weather = tweet.text
        print(tweet.text)


# In[24]:


# Url to Mars facts website
mars_facts_url = 'https://space-facts.com/mars/'


# In[25]:


# Get table from url
mars_facts_table = pd.read_html(mars_facts_url)
mars_facts_table


# In[26]:


# Select table
mars_facts = mars_facts_table[0]

# Switch columns and rows
mars_facts_df = mars_facts.transpose()
mars_facts_df


# In[27]:


# Rename columns
mars_facts_df.columns = [
    'Equatorial diameter',
    'Polar diameter',
    'Mass',
    'Moons',
    'Orbit distance',
    'Orbit period',
    'Surface temperature',
    'First record',
    'Recorded by'
]

mars_facts_df


# In[28]:


# Get rid of first row
clean_mars_facts_df = mars_facts_df.iloc[1:]
clean_mars_facts_df


# In[29]:



# Print dataframe in html format# Print  
mars_facts_html_table = clean_mars_facts_df.to_html()
print(mars_facts_html_table)


# In[30]:



# Use splinter to get image and title links of each hemisphere# Use sp 
usgs_browser = Browser('chrome', headless=False)
usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
usgs_browser.visit(usgs_url)


# In[31]:


# Parse html file with BeautifulSoup
mars_hemispheres_html = usgs_browser.html
mars_hemispheres_soup = BeautifulSoup(mars_hemispheres_html, 'html.parser')


# In[32]:


# Print body of html
print(mars_hemispheres_soup.body.prettify())


# In[33]:



# Find hemisphere image link and title# Find h 
mars_hemispheres = mars_hemispheres_soup.find_all('div', class_='description')
mars_hemispheres


# In[34]:


# Create list of dictionaries to hold all hemisphere titles and image urls
hemisphere_image_urls = []

# Loop through each link of hemispheres on page
for image in mars_hemispheres:
    hemisphere_url = image.find('a', class_='itemLink')
    hemisphere = hemisphere_url.get('href')
    hemisphere_link = 'https://astrogeology.usgs.gov' + hemisphere
    print(hemisphere_link)

    # Visit each link that you just found (hemisphere_link)
    usgs_browser.visit(hemisphere_link)
    
    # Create dictionary to hold title and image url
    hemisphere_image_dict = {}
    
    # Need to parse html again
    mars_hemispheres_html = usgs_browser.html
    mars_hemispheres_soup = BeautifulSoup(mars_hemispheres_html, 'html.parser')
    
    # Get image link
    hemisphere_link = mars_hemispheres_soup.find('a', text='Original').get('href')
    
    # Get title text
    hemisphere_title = mars_hemispheres_soup.find('h2', class_='title').text.replace(' Enhanced', '')
    
    # Append title and image urls of hemisphere to dictionary
    hemisphere_image_dict['title'] = hemisphere_title
    hemisphere_image_dict['img_url'] = hemisphere_link
    
    # Append dictionaries to list
    hemisphere_image_urls.append(hemisphere_image_dict)

print(hemisphere_image_urls)


# In[35]:


# Convert this jupyter notebook file to a python script called 'scrape_mars.py'
get_ipython().system(' jupyter nbconvert --to script --template basic mission_to_mars.ipynb --output scrape_mars')

