import nltk
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer

train_file = state_union.raw('2005-GWBush.txt')
sample_file = state_union.raw('2006-GWBush.txt')

custom_sent_tokenizer = PunktSentenceTokenizer(train_file)
tokenized = custom_sent_tokenizer.tokenize(sample_file)


def process_content():
    try:
        for i in tokenized[:5]:
            words = nltk.word_tokenize(i)
            tagged = nltk.pos_tag(words)
            print(tagged)
    except Exception as e:
        print(str(e))

process_content()
