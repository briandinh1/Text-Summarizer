import sys
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import SnowballStemmer

class Summarizer:
    def __init__(self):
        # list of stopwords from nltk library
        self.stopWords = set(stopwords.words('english'))
        self.stemmer = SnowballStemmer('english')
        self.contents = '' # the original text
    
    def readFile(self, fileName):
        f = open(fileName, 'r')
        self.contents = f.read()
        f.close()

    # list of all words in the text
    def getWords(self):        
        return word_tokenize(self.contents.decode('utf-8', 'ignore'));

    #list of sentences in the text
    def getSentences(self):
        return sent_tokenize(self.contents.decode('utf-8', 'ignore'))

    def getWordFrequency(self, words): 
        frequency = {} # dictionary mapping words to their frequency
        for word in words:
            word = word.lower()
            if word in self.stopWords:
                continue # stop words add no value to sentence weight
            word = self.stemmer.stem(word) # only keep common prefixes of words
            if word in frequency:
                frequency[word] += 1
            else:
                frequency[word] = 1
        return frequency

    # extractive summarization method; no complicated machine learning stuff
    # assign values to sentences based on sum of its words' frequencies
    def scoreSentences(self, sentences, frequency):
        sentenceValues = {}
        for sentence in sentences: # loop each sentence
            for word, freq in frequency.iteritems(): # loop each word's frequency
                if word in sentence.lower(): # if the word is in the sentence
                    if sentence in sentenceValues: # add it to the current sum
                        sentenceValues[sentence] += freq;
                    else:
                        sentenceValues[sentence] = freq;
        return sentenceValues

    def generateSummary(self, lowerBound=0.8):
        # tokenize into words and sentences, then determine freq and sentence values
        words = self.getWords() 
        sentences = self.getSentences() 
        frequency = self.getWordFrequency(words)
        sentenceValues = self.scoreSentences(sentences, frequency)
        # minimum value of summary must be > some % of maximum sentence value
        highestValue = max(sentenceValues.values())
        threshold = int(lowerBound * highestValue)
        # then compare each sentence value with the threshold value
        summary = ''
        for sentence in sentences:
            if sentence in sentenceValues and sentenceValues[sentence] >= threshold:
                summary += ' ' + sentence;
        print(summary);
        


def main():
    summarizer = Summarizer()
    summarizer.readFile('sample.txt')
    summarizer.generateSummary()
    
if __name__ == "__main__":
    main()




