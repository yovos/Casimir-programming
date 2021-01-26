import re
import collections
import matplotlib.pyplot as plt
import numpy as np
import nltk
from nltk import tokenize
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')


stop_words=set(stopwords.words("english"))
print(stop_words)

#file = open("test.txt", "r")
file = open("war_and_peace.txt", "r")

data = file.read()
data_wout_symbols = re.sub(r'[^\w]', ' ', data) #remove symbols
words = data_wout_symbols.split() #split text at space
sentences = tokenize.sent_tokenize(data)

for i in range(len(words)):
    #make all words lowercase
    words[i] = words[i].lower()

#print(words)
print('Number of words:', len(words)) #How many words are there in total in the txt file
print('Number of sentences:', len(sentences))
print('Average sentence length:', len(words)/len(sentences))
frequency_letter = collections.Counter(data_wout_symbols) #count how often each letter occurs
frequency_words = collections.Counter(words) #count how often each word occurs
#print(frequency_letter) #print all letters and how oftern they occur
#print(frequency_words.most_common(5)) #print x most common words
#print(frequency_words.most_common()[-1]) #print word at the end of the list
#print(frequency_words['war'],frequency_words['peace']) #print frequency of given word


#We now do statistics with the N most common words
#

N = 1000

frequency_words_decreasing = collections.OrderedDict(frequency_words.most_common(N)) #most_common returns list and we convert it back into an ordered dictionary for the diagram to work
frequency_percentage = [(i, frequency_words[i] / len(words) * 100.0) for i,count in frequency_words.most_common(N)] #Compute with what percentage the words occur
frequency_percentage_decreasing = collections.OrderedDict(frequency_percentage) #Make ordered dictionary of most common words and with which percentage they occur
#print(frequency_percentage[:5]) #print the five most common words with percentage 

fig, axes = plt.subplots()
#Log-Log plot of frequency with which common words occur and their rank
axes.set_xscale('log')
axes.set_yscale('log')
axes.set_xlabel(r'Rank', size=15)
axes.set_ylabel(r'Frequency', size=15)
axes.plot(np.arange(0,N,1), frequency_percentage_decreasing.values())
#list(frequency_percentage_decreasing).index('is') #Position of a given word in list of most common words
#plt.bar(frequency_percentage_decreasing.keys(), frequency_percentage_decreasing.values())
plt.savefig('diagram.png')