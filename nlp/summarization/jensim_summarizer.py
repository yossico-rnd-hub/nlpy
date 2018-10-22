from gensim.summarization import summarize as gensim_summarize


class Summarization(object):
    def summarize(self, text, word_count=50):
        res = gensim_summarize(text, word_count=word_count)
        return res
