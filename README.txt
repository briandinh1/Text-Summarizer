A text summarizer program in python using the NLTK library. GUI EXE for demo
It's based on an extractive summarization algorithm

Run every word through a stemmer, to get to the base words (dog = dogs, doggies, etc)
Count the frequency of each word in the text. Discard stop words because they add no value to the weight of a sentence
Then for each sentence, calculate sentence value according to the its words' frequencies
Choose words to use in the final summary by comparing every sentence's value with a threshold value
Threshold is 80% of the highest valued sentence. Percentage can be changed in the GUI. 
For longer texts I found 0.8 is good. crank it up to 90% for very brief summaries (sometimes produces 1 or 2 sentences only)