import urllib.request
import numpy as np
from lxml import html
from string import digits
import os
import pandas as pd
import re

remove_digits = str.maketrans('', '', digits)  

if not os.path.isdir('books') :
    os.mkdir('books')
    

def get_bookinfo_from_xpath(htmltree, xpath, special_characters = ["\n", "\t", ",", "'", "-", ":", ";", "(", ")", ".", "?", '\r']): 
    """
    Returns information about the book's webpage using an htmltree,
    and an xpath to select the approriate web elemen. Removes any weird
    character from the obtained data.
    
    Params:
        htmltree: parsed html page
        xpath: xpath query
        
    returns string of book info
    """
    
    #Use .xpath to get the selected webelement using the xpath
    info = htmltree.xpath(xpath)
    info = "".join(info) #flatten the list
    
    #Loop through every special character and remove each
    for char in special_characters:
        info = info.replace(char, '')
    
    return info


def get_info_book(htmltree):

    title = get_bookinfo_from_xpath(htmltree, "//td[@itemprop='headline']/text()", ["\n", "\t", "\r"])
    
    author = get_bookinfo_from_xpath(htmltree, "//a[@itemprop='creator']/text()")
    author = author.translate(remove_digits) #Remove digits since author's birthdate are also included
    
    year = get_bookinfo_from_xpath(htmltree, "//a[@itemprop='creator']/text()", ["\n", "\t"])
    year = re.findall(r'\b\d+\b', year) #Extract digits to get the author's years
    if not year:
        year = 'unknown'
    else:
        try:
            year = year[0] + '-' + year[1]
        except IndexError:
            year = year[0]

    subjects = htmltree.xpath("//td[@property='dcterms:subject']/a/text()")
    subjects = [s.replace('\n', '') for s in subjects]
    
    title_filename = get_bookinfo_from_xpath(htmltree, "//td[@itemprop='headline']/text()")
    author_filename = get_bookinfo_from_xpath(htmltree, "//a[@itemprop='creator']/text()")
    author_filename = author_filename.translate(remove_digits) #Remove digits since author's birthdate are also included
    filename = title_filename.lower() + " " + author_filename.lower()
    filename = filename.replace(" ", "-")[:-1] + ".txt"
    filename = os.path.join('./books', filename)
    
    
    info_dict = {
        'Title': title,
        'Author': author,
        'Year': year,
        'Subjects': subjects,
        'Filename': filename,
    }
    
    return info_dict
        
def save_book_txt(htmltree):
    """
    Save the book to a .txt file from Gutenberg project.
    
    Parameters:
        url: Gutenberg webpage of a specific book e.g. https://www.gutenberg.org/ebooks/1342
    
    Return
        Saves to a .txt file with pattern title-author in lowercase
    """
    home_url = 'https://www.gutenberg.org'
    

    #Get the href to .txt file    
    data = htmltree.xpath("//td/text()")
    filelink = [tc for tc in data if '.txt' in tc ]
    if not filelink:
        print('No .txt file for {}'.format(href))

    #Load book and author information
    title = get_bookinfo_from_xpath(htmltree, "//td[@itemprop='headline']/text()")
    author = get_bookinfo_from_xpath(htmltree, "//a[@itemprop='creator']/text()")
    author = author.translate(remove_digits) #Remove digits since author's birthdate are also included

    #Load book .txt webpage
    booktext = urllib.request.urlopen(filelink[0]).read().decode('utf8')
    
    #Define the filename as title-author.txt
    filename = title.lower() + " " + author.lower()
    filename = filename.replace(" ", "-")[:-1] + ".txt"
    filename = os.path.join('./books', filename)
    
    #Save webpage to a .txt file with title-author as name in the books folder
    txt_file = open(filename, "wt")
    n = txt_file.write(booktext)
    txt_file.close()

    
    

def list_book_info():
    """
    Lists title, author, year author, genre and filename of each book in the Gutenberg top 100 downloaded. 
    
    returns pandas dataframe with the info.
    """
    # #Homepage of gutenberg project
    home_url = 'https://www.gutenberg.org'
    bookinfo_list = []

    # Load all urls of the top 100 downloaded books from gutenberg
    url = 'https://www.gutenberg.org/browse/scores/top'
    
    #Request the url and decode it to text
    text = urllib.request.urlopen(url).read().decode('utf8')

    #Generate a html tree to filter the proper hrefs
    htmltree = html.fromstring(text)

    #filter the top 100 books hrefs from the page's first ordered list
    hrefs = htmltree.xpath("/html/body/div/div[1]/ol[1]//a/@href")

    #Loop through each book's page to get the .txt file and book info
    for href in hrefs:
        
        #Create url of bookpage
        bookinfo_url = home_url + href

        #Parse the bookinfo html page
        bookinfo = urllib.request.urlopen(bookinfo_url).read().decode('utf8')
        htmltree = html.fromstring(bookinfo)
        
        bookinfo_list.append(get_info_book(htmltree))
        
    return pd.DataFrame(bookinfo_list)
        
        
def save_top100_to_txt():
    # #Homepage of gutenberg project
    home_url = 'https://www.gutenberg.org'
    bookinfo_list = []

    # Load all urls of the top 100 downloaded books from gutenberg
    url = 'https://www.gutenberg.org/browse/scores/top'
    
    #Request the url and decode it to text
    text = urllib.request.urlopen(url).read().decode('utf8')

    #Generate a html tree to filter the proper hrefs
    htmltree = html.fromstring(text)

    #filter the top 100 books hrefs from the page's first ordered list
    hrefs = htmltree.xpath("/html/body/div/div[1]/ol[1]//a/@href")

    #Loop through each book's page to get the .txt file and book info
    for href in hrefs:
        
        #Create url of bookpage
        bookinfo_url = home_url + href

        #Parse the bookinfo html page
        bookinfo = urllib.request.urlopen(bookinfo_url).read().decode('utf8')
        htmltree = html.fromstring(bookinfo)
        
        save_book_txt(htmltree)

        
#df = list_book_info()       
#df.to_csv(r'Books_Dataframe.csv')