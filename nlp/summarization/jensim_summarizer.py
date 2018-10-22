#!env/bin/python

from gensim.summarization import summarize as gensim_summarize


class Summarization(object):
    def summarize(self, text, word_count=50):
        res = gensim_summarize(text, word_count=word_count)
        return res

# lilo
# with open('./tests/docs/text4', 'r') as f:
#     text = f.read()
#     print(gensim_summarize(text, word_count=50))
