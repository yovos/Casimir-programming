import re
import collections
import matplotlib.pyplot as plt
import numpy as np
import nltk
from nltk import tokenize
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')
import ast
import pandas as pd

#######################################################################################################
#Get filename from entered title
#######################################################################################################


def get_filename_from_title(title):
    File_100_Books = open("books_dictionary.txt", "r")
    Contents_100_Books = File_100_Books.read()
    Dictionary_100_Books = ast.literal_eval(Contents_100_Books)
    File_100_Books.close()
    #print(Dictionary_100_Books[2]['Title'])
    for i in range(len(Dictionary_100_Books)):
        if Dictionary_100_Books[i]['Title'] == title:
            return Dictionary_100_Books[i]['Filename']

<<<<<<< HEAD
def get_list_words_from_title():
    #print(get_filename_from_title("War and Peace"))
    Title_entered = input("Enter title: " )
    filename = get_filename_from_title(Title_entered)
    #print(filename)
    #file = open("test.txt", "r")
    if filename is not None:
        file = open(filename, "r")
    else:
        print("Title was not found.")
        exit()
    data = file.read()
    data_wout_symbols = re.sub(r'[^\w]', ' ', data) #remove symbols
    words = data_wout_symbols.split() #split text at space
    return data_wout_symbols, words
=======

#print(get_filename_from_title("War and Peace"))
Title_entered = input("Enter title: " )
filename = get_filename_from_title(Title_entered)
#print(filename)

#file = open("test.txt", "r")
if filename is not None:
    file = open(filename, "r")
else:
    print("Title was not found.")
    exit()
data = file.read()
data_wout_symbols = re.sub(r'[^\w]', ' ', data) #remove symbols
words = data_wout_symbols.split() #split text at space
sentences = tokenize.sent_tokenize(data)
>>>>>>> 929b8dbeddb0995ce971e1690f32d278ba94ec90


#######################################################################################################
#Get list of words, count how often they appear and plot rank v frequency
#######################################################################################################

data_wout_symbols, words = get_list_words_from_title()

for i in range(len(words)): 
    #make all words lowercase
    words[i] = words[i].lower()

Count_of_letter = collections.Counter(data_wout_symbols) #count how often each letter occurs
Count_of_words = collections.Counter(words) #count how often each word occurs

#print(words) #Print all words
#print('Number of words:', len(words)) #How many words are there in total in the txt file
#print(frequency_letter) #print all letters and how oftern they occur
#print(Count_of_words.most_common(5)) #print x most common words
#print(Count_of_words.most_common()[-1]) #print word at the end of the list
#print(Count_of_words['war'],Count_of_words['peace']) #print frequency of given word

def Rank_Frequency_Plot(N):
    """
    Plot of rank v frequency of N most common words in text
    """
    Most_common_words_decreasing = collections.OrderedDict(Count_of_words.most_common(N)) #most_common returns list and we convert it back into an ordered dictionary for the diagram to work
    Frequency_common_words = [(i, Count_of_words[i] / len(words) * 100.0) for i,count in Count_of_words.most_common(N)] #Compute with what percentage the words occur
    Frequency_common_words_decreasing = collections.OrderedDict(Frequency_common_words) #Make ordered dictionary of most common words and with which percentage they occur
    #print(frequency_percentage[:5]) #print the five most common words with percentage 

    fig, axes = plt.subplots()
    axes.set_xscale('log')
    axes.set_yscale('log')
    axes.set_xlabel(r'Rank', size=15)
    axes.set_ylabel(r'Frequency', size=15)
    axes.plot(np.arange(0,N,1), Frequency_common_words_decreasing.values())
    #list(frequency_percentage_decreasing).index('is') #Position of a given word in list of most common words
    #plt.bar(frequency_percentage_decreasing.keys(), frequency_percentage_decreasing.values())
    plt.savefig('diagram.png')
    
Rank_Frequency_Plot(3000)
#Rank_Frequency_Plot(len(Count_of_words))
print(len(Count_of_words)/len(words)) #Number of unique words/Number total words
print('Number of sentences:', len(sentences))