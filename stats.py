import re
import collections
import matplotlib.pyplot as plt
import numpy as np
#import nltk
#from nltk import tokenize
#from nltk.corpus import stopwords
#nltk.download('punkt')
#nltk.download('stopwords')
import ast
import pandas as pd
import os.path

#######################################################################################################
#Get filename from entered title
#######################################################################################################


stop_words=set(stopwords.words("english"))

def get_filename_from_title(title):
    File_100_Books = open("books_dictionary.txt", "r")
    Contents_100_Books = File_100_Books.read()
    Dictionary_100_Books = ast.literal_eval(Contents_100_Books)
    File_100_Books.close()
    #print(Dictionary_100_Books[2]['Title'])
    for i in range(len(Dictionary_100_Books)):
        if Dictionary_100_Books[i]['Title'] == title:
            return Dictionary_100_Books[i]['Filename']


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

def get_list_words_from_filename(filename):
    file = open(filename, "r")
    data = file.read()
    data_wout_symbols = re.sub(r'[^\w]', ' ', data) #remove symbols
    words = data_wout_symbols.split() #split text at space
    return data_wout_symbols, words


#######################################################################################################
#Get list of words, count how often they appear and plot rank v frequency
#######################################################################################################

#BEGIN data_wout_symbols, words = get_list_words_from_title()

# for i in range(len(words)): 
#     #make all words lowercase
#     words[i] = words[i].lower()

# Count_of_letter = collections.Counter(data_wout_symbols) #count how often each letter occurs
#END Count_of_words = collections.Counter(words) #count how often each word occurs

#print(words) #Print all words
#print('Number of words:', len(words)) #How many words are there in total in the txt file
Count_of_letter = collections.Counter(data_wout_symbols) #count how often each letter occurs
Count_of_words = collections.Counter(words) #count how often each word occurs
avg_sen_length = len(sentences)/len(words)

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

    #fig, axes = plt.subplots()
    axes.set_xscale('log')
    axes.set_yscale('log')
    axes.set_xlabel(r'Rank', size=15)
    axes.set_ylabel(r'Frequency', size=15)
    axes.plot(np.arange(0,N,1), Frequency_common_words_decreasing.values())
    #list(frequency_percentage_decreasing).index('is') #Position of a given word in list of most common words
    #plt.bar(frequency_percentage_decreasing.keys(), frequency_percentage_decreasing.values())
    #!!!plt.savefig('diagram.png')
    
#!!!Rank_Frequency_Plot(3000)
#Rank_Frequency_Plot(len(Count_of_words))
#print(len(Count_of_words)/len(words)) #Number of unique words/Number total words
#print('Number of sentences:', len(sentences))


#######################################################################################################
#Add statistics to all books in dataframe
#######################################################################################################

fig, axes = plt.subplots()
Books_dataframe = pd.read_csv("Books_Dataframe.csv") 
#print(Books_dataframe)
list_number_of_words = []
#most_common_letters = []
most_common_words = []
most_diverse = []
for i in range(100):
    #print(Books_dataframe.iloc[i,5])
    filename = Books_dataframe.iloc[i,5]
    #filename = '/' + filename.lstrip('./') #remove leading dot in filename
    if os.path.exists(filename):
        data_wout_symbols, words = get_list_words_from_filename(filename)
        for j in range(len(words)):
            #make all words lowercase
            words[j] = words[j].lower()
        Count_of_letter = collections.Counter(data_wout_symbols) #count how often each letter occurs
        Count_of_words = collections.Counter(words) #count how often each word occurs
        list_number_of_words.append(len(words))
        #most_common_letters.append(Count_of_letter.most_common(2))
        most_common_words.append(list(collections.OrderedDict(Count_of_words.most_common(2)).keys()))
        most_diverse.append(len(Count_of_words)/len(words))
        #Rank_Frequency_Plot(1000)
    else:
        list_number_of_words.append("File not found")
        most_common_words.append("File not found")
        #most_common_letters.append("File not found")
        most_diverse.append(0)
Books_dataframe['Total Number Words'] = list_number_of_words
#Books_dataframe['Two Most Common Letters'] = most_common_letters
Books_dataframe['Two Most Common Words'] = most_common_words
Books_dataframe['Ratio of Unique and Total Words'] = most_diverse
Books_dataframe.to_csv(r'Books_w_stats.csv', index = False)
max_index = pd.to_numeric(Books_dataframe['Ratio of Unique and Total Words']).idxmax()
print(Books_dataframe.iloc[max_index,1])
#plt.savefig('diagram.png')
