A text summarizer program in python using the NLTK library. GUI EXE for demo

Run every word through a stemmer, to get to the base words (dog = dogs, doggies, etc)
Count the frequency of each word in the text. Discard stop words, provided by NLTK, because they add no value to the weight of a sentence
Then for each sentence in the text, build a sentence value for it according to the value of its words' frequencies
The summarizer chooses words to use in the final summary by comparing every sentence's value with a predetermined threshold value.
Threshold is based on the sentence with the highest value multiplied by 80% (by default, only sentences with values >= 80% of the max value are considered)
The percentage can be changed in the GUI. For longer texts I found 0.8 is good. crank it up to 90% for very brief summaries (sometimes 1 or 2 sentences only)