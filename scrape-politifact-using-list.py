# Page list goes from 1 to 879
# the url for scraping is: 'https://www.politifact.com/factchecks/list/?page={}' with page number between 1 and 879

# Import the dependencies
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time

# Create lists to store the scraped data
authors = []
statement_dates = []
factcheck_dates = []
statements = []
sources = []
verdicts = []
urls = []
tags = []
contexts = []

def scrape_website(page_number, start_time):
    page_num = str(page_number) # Convert the page number to a string

    '''source: all'''
    # URL = 'https://www.politifact.com/factchecks/list/?page='+page_num # Append the page number to complete the URL
    URL = 'https://www.politifact.com/factchecks/list/?page={}'.format(page_num)
    print(URL)

    webpage = requests.get(URL)  # Make a request to the website
    soup = BeautifulSoup(webpage.text, "html.parser") #Parse the text from the website

    # Get the tags and it's class
    statement_footer =  soup.find_all('footer',attrs={'class':'m-statement__footer'})  # Get the tag and it's class
    statement_quote = soup.find_all('div', attrs={'class':'m-statement__quote'}) # Get the tag and it's class
    statement_meta = soup.find_all('div', attrs={'class':'m-statement__meta'})# Get the tag and it's class
    target = soup.find_all('div', attrs={'class':'m-statement__meter'}) # Get the tag and it's class

    # Loop through the footer class m-statement__footer to get the author
    for i in statement_footer:
        footer_text = i.text.strip()
        # Format: "By [Name] • [Date]"
        # Split by bullet point to separate name and date
        if '•' in footer_text:
            parts = footer_text.split('•')
            # Extract name (remove "By " prefix)
            full_name = parts[0].replace('By', '').strip()
            authors.append(full_name)
            # Extract date (after bullet point)
            factcheck_date = parts[1].strip()
            factcheck_dates.append(factcheck_date)
        else:
            # Fallback if bullet point not found
            authors.append('')
            factcheck_dates.append('')

    # Loop through the div m-statement__quote to get the statement and URL
    for i in statement_quote:
        link2 = i.find_all('a')
        statements.append(link2[0].text.strip())

        # Extract the href attribute and create full URL
        href = link2[0].get('href')
        full_url = 'https://www.politifact.com' + href
        urls.append(full_url)

        # Extract tags, date, and context from the individual article page
        webpage_article = requests.get(full_url)
        soup_article = BeautifulSoup(webpage_article.text, "html.parser")
        
        # Extract date and context from m-statement__desc
        statement_desc = soup_article.find('div', attrs={'class': 'm-statement__desc'})
        if statement_desc:
            desc_text = statement_desc.text.strip()
            # Pattern: "stated on [DATE] in [CONTEXT]:"
            if ' in ' in desc_text and ' on ' in desc_text:
                # Extract date (between "on" and "in")
                date_part = desc_text.split(' on ')[1].split(' in ')[0].strip()
                statement_dates.append(date_part)
                # Extract context (between "in" and ":")
                context_part = desc_text.split(' in ')[1].split(':')[0].strip()
                # Remove leading articles/prepositions
                for prefix in ['an ', 'a ', 'the ', 'in ']:
                    if context_part.lower().startswith(prefix):
                        context_part = context_part[len(prefix):]
                        break
                contexts.append(context_part)
            else:
                statement_dates.append('')
                contexts.append('')
        else:
            statement_dates.append('')
            contexts.append('')
        
        # Find the ul element with class m-list m-list--horizontal
        tag_list = soup_article.find('ul', attrs={'class': 'm-list m-list--horizontal'})
        article_tags = []
        
        if tag_list:
            # Find all li elements within the ul
            tag_items = tag_list.find_all('li', attrs={'class': 'm-list__item'})
            for tag_item in tag_items:
                # Find the a tag with class c-tag
                tag_link = tag_item.find('a', attrs={'class': 'c-tag'})
                if tag_link:
                    # Check if it's not a personality tag (personality tags have /personalities/ in href)
                    href = tag_link.get('href', '')
                    if '/personalities/' not in href:
                        # Extract the span text
                        tag_span = tag_link.find('span')
                        if tag_span:
                            article_tags.append(tag_span.text.strip())
        
        # Join tags with a semicolon or comma
        tags.append('; '.join(article_tags) if article_tags else '')
        
        # Add a small delay to be respectful to the server (so you don't get blocked)
        time.sleep(0.2)

    # Loop through the div m-statement__meta to get the source
    for i in statement_meta:
        link3 = i.find_all('a') #Source
        source_text = link3[0].text.strip()
        sources.append(source_text)

    # Loop through the target or the div m-statement__meter to get the facts about the statement (True or False)
    for i in target:
        fact = i.find('div', attrs={'class':'c-image'}).find('img').get('alt')
        if fact == 'barely-true':
            fact = 'mostly-false'
        verdicts.append(fact)
    
    # Print elapsed time
    elapsed_time = time.time() - start_time
    print(f"Page {page_number} completed. Elapsed time: {elapsed_time:.2f} seconds")

# Loop through 'n-1' webpages to scrape the data
start_time = time.time()
n=5
for i in range(1, n):
    scrape_website(i, start_time)

# Create a new dataFrame
data = pd.DataFrame(columns = ['statement_originator', 'statement_date', 'statement', 'verdict', 'statement_source', 'tags', 'factchecker', 'factcheck_date', 'factcheck_analysis_link'])
data['factchecker'] = authors
data['statement'] = statements
data['statement_originator'] = sources
data['statement_date'] = statement_dates
data['statement_source'] = contexts
data['verdict'] = verdicts
data['factcheck_date'] = factcheck_dates
data['factcheck_analysis_link'] = urls
data['tags'] = tags

# Show the data set
data.iloc[:].to_csv('politifact.csv', index=False, sep=',')