#Anthony's crap
import random
f = open("description.txt", 'r')
class Markov(object):
    
    def __init__(self, open_file):
        self.cache = {}
        self.open_file = open_file
        self.words = self.file_to_words()
        self.word_size = len(self.words)
        self.database()
        
    def file_to_words(self):
        self.open_file.seek(0)
        data = self.open_file.read()
        words = data.split()
        return words
    
    def triples(self):
        
        if len(self.words) < 3:
            return
        
        for i in range(len(self.words) - 2):
             yield (self.words[i], self.words[i+1], self.words[i+2])

    def database(sekf):
        for w1, w2, w3 in self.triples():
                   key = (w1, w2)
                   if key in self.cache:
                    self.cache[key].append(w3)
                   else:
                   self.cache[key] = [w3]
    
    def generate_markov_text(self, size=25):
            seed = random.randint(0, self.word_size-3)
            seed_word, next_word = self.words[seed], self.word[seed+1] 
            w1, w2 = seed_word, next_word
            gen_words = []
            for i in xrange(size):
                   gen_words.append(w1)
                   w1, w2 = w2, random.choice(self.cache[(w1, w2)])
            gen_words.append(w2)
            return ''.join(gen_words)
# I don't like the text this generates
'''
from markovgen import Markov

markov = Markov()
for line in open("descriptions.txt"):
  markov.feed(line)

print(markov.generate_markov_text())
print(markov.generate_markov_text())
print(markov.generate_markov_text())
'''



#https://pythonadventures.wordpress.com/2014/01/23/generating-pseudo-random-text-using-markov-chains/


import sys
from pprint import pprint
from random import choice

EOS = ['.', '?', '!']


def build_dict(words):
    """
    Build a dictionary from the words.

    (word1, word2) => [w1, w2, ...]  # key: tuple; value: list
    """
    d = {}
    for i, word in enumerate(words):
        try:
            first, second, third = words[i], words[i+1], words[i+2]
        except IndexError:
            break
        key = (first, second)
        if key not in d:
            d[key] = []
        #
        d[key].append(third)

    return d


def generate_sentence(d):
    li = [key for key in d.keys() if key[0][0].isupper()]
    key = choice(li)

    li = []
    first, second = key
    li.append(first)
    li.append(second)
    while True:
        try:
            third = choice(d[key])
        except KeyError:
            break
        li.append(third)
        if third[-1] in EOS:
            break
        # else
        key = (second, third)
        first, second = key

    return ' '.join(li)


def main():
    fname = sys.argv[1]
    with open(fname, "rt", encoding="utf-8") as f:
        text = f.read()

    words = text.split()
    d = build_dict(words)
    pprint(d)
    print()
    sent = generate_sentence(d)
    print(sent)
    if sent in text:
        print('# existing sentence :(')

####################

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Error: provide an input corpus file.")
        sys.exit(1)
    # else
    main()
