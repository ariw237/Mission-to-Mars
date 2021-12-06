#Import our dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    #Set a path to chrome and setup our url
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    news_title, news_paragraph = mars_news(browser)
    #Run all scraping fucntions and store results in dictionary
    data = {
     "news_title": news_title,
     "news_paragraph": news_paragraph,
     "featured_image": featured_image(browser),
     "facts" : mars_facts(),
     "last_modified" : dt.datetime.now(),
     "hemispheres" : mars_hemispheres(browser)
    }
    browser.quit()
    return data
def mars_news(browser):

#Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
#set a slight delay in page loading
    browser.is_element_present_by_css('div.list_text', wait_time=1)
# The final line of code in above code searches tag: div and with class: item_list

#Set up HTML parser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    try:
        slide_elem = news_soup.select_one('div.list_text') #The parent element is stored in slide_elem
#Obtain the title of the first article:
        slide_elem.find('div', class_='content_title')
#Filter to get just the text of the title:
        news_title = slide_elem.find('div', class_='content_title').get_text()
    #Get the summary of the first article
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None

    return news_title, news_p
#Scrape mars images webpage

#find and click the full image button
def featured_image(browser):
    url = 'https://spaceimages-mars.com'
    browser.visit(url)


    full_image_elem = browser.find_by_tag('button')[1] #First button element in webpage html
    full_image_elem.click()
    html = browser.html
    img_soup = soup(html, 'html.parser')

#Find the relative (featured) image url:
    try:
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        img_url_rel
#Note that get('src') pulls a link to that image

#Now we need to add this to the base url to get a complete url:
        img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    except AttributeError:
        return None
    return img_url

#We are now going to scrape the mars facts table from https://galaxyfacts-mars.com/
#read_html will automatically print all tables found in a particular html
def mars_facts():
    try:
        df = pd.read_html('https://galaxyfacts-mars.com/')[0]  #The zero tell pandas to import first table it sees
    except BaseException:
        return None
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace = True)

#We can convert the dataframe back to html format:
    return df.to_html()
#End our session (very important as it shuts down the automated browser)
def mars_hemispheres(browser):
    hemisphere_image_urls = []
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    html = browser.html
    mars_hemi = soup(html, 'html.parser')
    div_descriptions = mars_hemi.find_all('div', class_= 'description')

    def get_hemisphere_data(description):
        title = description.find('h3').get_text()
        hemi_link = description.find('a', class_= 'itemLink product-item').get('href')
        hemi_link_url = f'{url}{hemi_link}'
        browser.visit(hemi_link_url)
        html = browser.html
        mars_img = soup(html, 'html.parser')
        div_download = mars_img.find('div', class_='downloads')
        image_href = div_download.find('a').get('href')
        link = f'{url}{image_href}'
        return title, link

    for div_description in div_descriptions:
        hemispheres = {}
        get_hemisphere_data(div_description)
        hemispheres['title'] = get_hemisphere_data(div_description)[0]
        hemispheres['image_url'] = get_hemisphere_data(div_description)[1]
        hemisphere_image_urls.append(hemispheres)

    return hemisphere_image_urls


if __name__ == "__main__":
    print(scrape_all())
