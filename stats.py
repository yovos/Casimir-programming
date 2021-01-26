import re
import collections
import matplotlib.pyplot as plt
import numpy as np


#file = open("test.txt", "r")
file = open("war_and_peace.txt", "r")

data = file.read()
data_wout_symbols = re.sub(r'[^\w]', ' ', data) #remove symbols
words = data_wout_symbols.split() #split text at space

for i in range(len(words)):
    #make all words lowercase
    words[i] = words[i].lower()

#print(words)
print('Number of words:', len(words))
frequency_letter = collections.Counter(data_wout_symbols) #count how often each letter occurs
frequency_words = collections.Counter(words) #count how often each word occurs
#print(frequency_letter) #print frequency of letters
print(frequency_words.most_common(5)) #print x most common words
print(frequency_words.most_common()[-1]) #print word at the end of the list
print(frequency_words['war'],frequency_words['peace']) #print frequency of given word
frequency_words_decreasing = collections.OrderedDict(frequency_words.most_common(1000)) #Most common returns list and we convert it back into an ordered dictionary for the barchart to work

N = 1000

frequency_percentage = [(i, frequency_words[i] / len(words) * 100.0) for i,count in frequency_words.most_common(N)]
frequency_percentage_decreasing = collections.OrderedDict(frequency_percentage)

print(frequency_percentage[:5])

fig, axes = plt.subplots()

axes.set_xscale('log')
axes.set_yscale('log')
axes.plot(np.arange(0,N,1), frequency_percentage_decreasing.values())
#axes.plot(list(frequency_percentage_decreasing).index('is'), frequency_percentage_decreasing.values())
#axes.plot(frequency_percentage_decreasing.keys(), frequency_percentage_decreasing.values())
#plt.bar(frequency_percentage_decreasing.keys(), frequency_percentage_decreasing.values())
plt.savefig('bardiagram.png')

#Do plot showing Zipfs Distribution