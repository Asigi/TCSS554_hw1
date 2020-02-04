
# Arshdeep Singh
# TCSS 554 A


from nltk.stem.snowball import SnowballStemmer
import os
import re #Regular Expressions
import string

Stemmer_g = SnowballStemmer("english")

pyFileDir = os.path.dirname(os.path.realpath('__file__')) #the filepath of this python file.
vlogFolder = os.path.join(pyFileDir, "transcripts/")
stopFile = os.path.join(pyFileDir, "stopwords.txt")

WordDict_g = [] #dictionary for entire set of vlogs
WordDict_g_counts = {} #number of appearances for each unique word in the entire set of vlogs

VlogWordCount_g = [] #list containing lengths of vlogs before processing (not unique words)
PostProcessAllCount_g = [] #list containing lengths of each vlog after processing (not unique words)
VlogFullText = [] #each position contains full vlog text as a single string

remove = string.punctuation #used for removing special characters
remove = remove.replace("'", "") # don't remove apostrophe
pattern = r"[{}]".format(remove) # create the pattern

#read in stopwords from stopwords.txt
Stopwords_g = [] #list of stopwords
stopfile=open(stopFile,"r") #open stopwords file
for line in stopfile:
    Stopwords_g.append(line.rstrip('\n')) #remove new line character




#-----------------------------------------------------------------------------------
#STEP ONE: calculate how many words there are prior to word processing

for vlog in os.listdir("transcripts/"): #loop through files in transcript folder
    vlogName = os.path.join(vlogFolder, vlog) #access vlog which is in a folder contained within same folder as this python file
    file=open(vlogName,"r") #open vlog file
    #print(vlogName) #TEST
    count = 0 #number of words in this vlog
    sscount = 0; #number of words in this vlog after stemming and stopword removing
    uniqueFileWords = [] #create empty list
    uniqueFileWords_counts = {} #holds the number of appearances in this vlog for each of the words in uniqueFileWords
    postProcessAllWords = []
    
    fileWordsStrings = "" #string of all words in vlog

    try:
        for line in file: #add words in file to fileWords list while also removing special characters.
            newLine = re.sub(pattern, "", line) #filter out special chars (except apost.)
            fileWordsStrings += newLine
            
        
        for fwsWord in fileWordsStrings.split():
            
            word1 = fwsWord.strip("'")
            word = re.sub('[0-9]+', '', word1)
        
            #do counting of unique words in this file
            if (word.lower() in uniqueFileWords):
                count +=1  #add to counter for each word in the file
                uniqueFileWords_counts[word.lower()] += 1
            else:
                uniqueFileWords.append(word.lower()) #add the downcased word to the unique words
                count +=1
                uniqueFileWords_counts[word.lower()] = 1
                
                
            #do the counting of (non-unique) all words after processing
            postStemword = Stemmer_g.stem(word)
            if (postStemword in Stopwords_g):
                pass #dont add to postProcessAllWords list
            else:
                postProcessAllWords.append(postStemword)
            
 
    except UnicodeDecodeError: #ignore hidden files on MacOS such as ".ds_store" file
        pass #do nothing of this error appears.

            
    #add unique words to global dictionary
    for uword in uniqueFileWords:
        if (uword in WordDict_g):
            WordDict_g_counts[uword] += uniqueFileWords_counts[uword]
        else:
            WordDict_g.append(uword)
            WordDict_g_counts[uword] = uniqueFileWords_counts[uword]
    
    VlogWordCount_g.append(count) #appends the total count of words from this vlog
    PostProcessAllCount_g.append(len(postProcessAllWords))
    VlogFullText.append(fileWordsStrings)
    file.close() #close file to save computer resources.
    

#Print out answer to Question 1
allWordCount = 0;
for num in VlogWordCount_g:
    allWordCount += num
print("The total number of words before text processing is:               ", allWordCount)
allPostProcWordCount = 0;


for num in PostProcessAllCount_g:
    allPostProcWordCount += num
print("The total number of words after text processing is:                ", allPostProcWordCount)

print()


#-----------------------------------------------------------------------------------
#STEP TWO: calculate how many unique words there are after word processing



ProcessedWordDict_g_count = {} #number of times each processed word appears in ProcessedWordDict_g
ProcessedWordDict_g = [] #list of processed words


for unpword in WordDict_g:
    if (unpword in Stopwords_g): #stopword removal
        pass #do nothing because its a stopword
    else:
        ppword = Stemmer_g.stem(unpword) #stem
        if (ppword in Stopwords_g): #check if stemmed word is a stopword
            pass #do nothing because its a stopword
        else:
            if (ppword in ProcessedWordDict_g):
                ProcessedWordDict_g_count[ppword] += WordDict_g_counts[unpword]
                
            else:
                ProcessedWordDict_g_count[ppword] = WordDict_g_counts[unpword]
                ProcessedWordDict_g.append(ppword)


#Print out answer to question 2
print("The total number of unique processed words is:                     ", len(ProcessedWordDict_g))
print()

#-----------------------------------------------------------------------------------
#STEP THREE: calculate number of words that only occur once in the database



single_word_count = 0
for wdg in WordDict_g:
    if (WordDict_g_counts[wdg] == 1):
        single_word_count += 1

print("The total number of words that appear once (pre-process):          ", single_word_count)





single_word_count2 = 0
for wdg2 in ProcessedWordDict_g:
    if (ProcessedWordDict_g_count[wdg2] == 1):
        #print(wdg2)
        single_word_count2 += 1
    
print("The total number of words that appear once (post-process):         ", single_word_count2)




print()
#-----------------------------------------------------------------------------------
#STEP FOUR: calculate average number of word tokens per document

print("Average number of word tokens per document is:                     ",allWordCount/len(VlogWordCount_g))

#-----------------------------------------------------------------------------------
#STEP FIVE: calculations for top 30 words.


#f = open("testingDict.txt", "w")
#single_word_count3 = 0
#for wdg3 in ProcessedWordDict_g:
#   if (ProcessedWordDict_g_count[wdg3] >= 490):
#
#        f.write(f"{wdg3}  {ProcessedWordDict_g_count[wdg3]}\n")
#        single_word_count3 += 1
#print("The total number of unique words that appear alot (post-process):  ", single_word_count3)
#f.close()

counttt = 0
for s in VlogFullText:
    if ("i'm" in s):
        counttt += 1
print("im", counttt)

counttt2 = 0
for s in VlogFullText:
    if ("know" in s):
        counttt2 += 1
print("know", counttt2)

counttt3 = 0
for s in VlogFullText:
    if ("really" in s):
        counttt3 += 1
print("really", counttt3)

counttt4 = 0
for s in VlogFullText:
    if ("don't" in s):
        counttt4 += 1
print("dont", counttt4)


counttt5 = 0
for s in VlogFullText:
    if ("get" in s):
        counttt5 += 1
print("get", counttt5)


counttt6 = 0
for s in VlogFullText:
    if ("video" in s):
        counttt6 += 1
print("video", counttt6)


counttt7 = 0
for s in VlogFullText:
    if ("uh" in s):
        counttt7 += 1
print("uh", counttt7)


counttt7 = 0
for s in VlogFullText:
    if ("think" in s):
        counttt7 += 1
print("think", counttt7)




