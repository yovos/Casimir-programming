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
    """
    Retrieve the book's title, author, year, subject and filename we store it in from the 
    book's parsed webpage.
    
    Parameters:
        -htmltree: Parsed webpage from a specific book.
        
    Returns:
        - info_dict: A dictionary containing
            * Title: Book's title
            * Author: Book's author
            * Year: Year of the book/author
            * Filename: lowercase title-author.txt where all special characters are removed
    """
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
        
def save_book_txt(htmltree, filename):
    """
    Save the book to a .txt file from Gutenberg project.
    
    Parameters:
        url: Gutenberg webpage of a specific book e.g. https://www.gutenberg.org/ebooks/1342
        filename: Name of the document you want the save the book as
    
    Return
        Saves a book on Gutenberg project to a .txt file 
    """
    home_url = 'https://www.gutenberg.org'
    
    data = htmltree.xpath("//td/text()")
    filelink = [tc for tc in data if '.txt' in tc ]
    if not filelink:
        print('No .txt file for {}'.format(filename))
    else:
        #Load book .txt webpage
        booktext = urllib.request.urlopen(filelink[0]).read().decode('utf8')

        #Save webpage to a .txt file with title-author as name in the books folder
        txt_file = open(filename, "wt")
        n = txt_file.write(booktext)
        txt_file.close()
    
    

def list_book_info(save=False):
    """
    Lists title, author, year author, genre and filename of each book in the Gutenberg top 100 downloaded. 
    
    Parameters:
        save (boolean): If true, saves books .txt webpage to a .txt file locally. 
    
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
        
        bookdict = get_info_book(htmltree)
        
        bookinfo_list.append(bookdict)

        if save:
            filename_book = bookdict["Filename"]
            save_book_txt(htmltree, filename_book)
        
    return pd.DataFrame(bookinfo_list)

#df = list_book_info()       
#df.to_csv(r'Books_Dataframe.csv')