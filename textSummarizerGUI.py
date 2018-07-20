import sys
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import SnowballStemmer
from Tkinter import *
import Tkinter, tkFileDialog
from ScrolledText import*


class Summarizer:
    def __init__(self):
        self.root = Tk()
        self.lowerBound = DoubleVar(value=0.8)
        self.fileName = "No files imported yet"
        self.statusBar = Label(self.root, bd=2, text=self.fileName, anchor=W)
        self.statusBar.pack(side=BOTTOM, fill=X)
        self.textBox = ScrolledText(self.root, height=18, width=47, bg="white", wrap=WORD, )
        self.textBox.pack(side=RIGHT, fill=X)
        self.root.title('NLTK Text Summarizer - Brian Dinh')
        self.root.minsize(width=550, height=350) # fixed height and width
        self.root.maxsize(width=550, height=350)
        self.leftFrame = Frame(self.root)
        self.leftFrame.pack(side=LEFT)
        self.entryBoxLabel = Label(self.leftFrame, text='Text Length: ', anchor=W)
        self.entryBoxLabel.pack(side=TOP)
        self.entryBox = Entry(self.leftFrame, textvariable=self.lowerBound, width=15, justify=CENTER)
        self.entryBox.pack(side=TOP)
        self.importButton = Button(self.leftFrame, text="Import Text", height=5, width=20, command=self.importText)
        self.importButton.pack(side=TOP, pady=7)
        self.generateButton = Button(self.leftFrame, text="Generate Text", height=5, width=20, command=self.generateSummary)
        self.generateButton.pack(side=TOP)
        # list of stopwords from nltk library
        self.stopWords = set(stopwords.words('english'))
        self.stemmer = SnowballStemmer('english')
        self.contents = '' # the original text
        
    def runGUI(self):
        self.root.mainloop()

    def generateSummary(self):
        summary = self.generate()
        self.textBox.delete(1.0, END)
        self.textBox.insert(INSERT, summary)

    def importText(self):
        fname = tkFileDialog.askopenfilename()
        if len(fname) > 0: # prevent file opener from overwriting existing
            self.fileName = fname
            self.readFile()
            currentFile = "Current File: " + self.fileName
            self.updateStatus()

    def updateStatus(self): # update status bar to show current file path
        self.statusBar.configure(text=self.fileName)

    def readFile(self):
        f = open(self.fileName, 'r')
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

    def generate(self):
        # tokenize into words and sentences, then determine freq and sentence values
        words = self.getWords() 
        sentences = self.getSentences() 
        frequency = self.getWordFrequency(words)
        sentenceValues = self.scoreSentences(sentences, frequency)
        # minimum value of summary must be > some % of maximum sentence value
        highestValue = max(sentenceValues.values())
        threshold = int(self.lowerBound.get() * highestValue)
        # then compare each sentence value with the threshold value
        summary = ''
        for sentence in sentences:
            if sentence in sentenceValues and sentenceValues[sentence] >= threshold:
                summary += ' ' + sentence;
        return summary



def main():
    summarizer = Summarizer()
    summarizer.runGUI()
    
if __name__ == "__main__":
    main()
