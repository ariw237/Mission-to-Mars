#Import our dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

#Set a path to chrome and setup our url
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

#Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
#set a slight delay in page loading
browser.is_element_present_by_css('div.list_text', wait_time=1)
# The final line of code in above code searches tag: div and with class: item_list

#Set up HTML parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text') #The parent element is stored in slide_elem

#Obtain the title of the first article:
slide_elem.find('div', class_='content_title')

#Filter to get just the text of the title:
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

#Get the summary of the first article
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

#Scrape mars images webpage
url = 'https://spaceimages-mars.com'
browser.visit(url)

#find and click the full image button
full_image_elem = browser.find_by_tag('button')[1] #First button element in webpage html
full_image_elem.click()
html = browser.html
img_soup = soup(html, 'html.parser')

#Find the relative (featured) image url:
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel
#Note that get('src') pulls a link to that image

#Now we need to add this to the base url to get a complete url:
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

#We are now going to scrape the mars facts table from https://galaxyfacts-mars.com/
#read_html will automatically print all tables found in a particular html
df = pd.read_html('https://galaxyfacts-mars.com/')[0]  #The zero tell pandas to import first table it sees
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace = True)
df
#We can convert the dataframe back to html format:
df.to_html()
#End our session (very important as it shuts down the automated browser)
browser.quit()
