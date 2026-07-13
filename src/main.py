import nltk
from nltk.tokenize import word_tokenize

english_sentence = "The child read."
tokens = word_tokenize(english_sentence)
tagged = nltk.pos_tag(tokens)
print(tagged)
