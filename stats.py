import re
from collections import Counter

#file = open("test.txt", "r")
file = open("war_and_peace.txt", "r")

data = file.read()
data_wout_symbols = re.sub(r'[^\w]', ' ', data)
words = data_wout_symbols.split()

for i in range(len(words)):
    #make all words lowercase
    words[i] = words[i].lower()

#print(words)
print('Number of words:', len(words))
frequency_letter = Counter(data_wout_symbols)
frequency_words = Counter(words)
#print(frequency_letter)
print(frequency_words.most_common(5))