import re
import collections
import matplotlib.pyplot as plt


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
print(frequency_words['war'],frequency_words['peace']) #print frequency of given word
frequency_words_decreasing = collections.OrderedDict(frequency_words.most_common(1000)) #Most common returns list and we convert it back into an ordered dictionary for the barchart to work
plt.bar(frequency_words_decreasing.keys(), frequency_words_decreasing.values())
plt.savefig('bardiagram.png')

