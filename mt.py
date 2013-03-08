import nltk
import sys
import collections


class Translation:
    def __init__(self, dict, originalText):
        self.dict = dict
        self.originalText = originalText
        self.englishText = []
        self.posText = []
    
    #Fills self.dict with a key value pair for every word    
    def engorge(self):
        SpanToEng = collections.defaultdict(lambda: '')
        
        dict = open(self.dict)
        for line in dict:
            key, value = line.split(',')
            key = key.lower()
            value = value.lower()
            SpanToEng[key] = value.rstrip('%\r\n')
            
        self.dict = SpanToEng
        #print self.dict
    
    def translate(self):
        spanishText = open(self.originalText)
        englishText = []
        for line in spanishText:
            englishLine = []
            for word in line.split():
                word = word.rstrip(' ,.:;').lower()
                word = word.lstrip()
                englishLine.append(self.dict[word])
            englishText.append(englishLine)
        
        self.englishText = englishText
        
       
    def POS(self):
        posText = []
        for line in self.englishText:
            for i in range(len(line)):
                line[i] = line[i].lstrip()
                line[i] = line[i].rstrip()
                
            posLine = nltk.pos_tag(line)
            posText.append(posLine)
        self.posText = posText
        
                
    def reallign(self):
        #Number 1 Rule: When PRP preceeds VB., switch them
        
        
        
        
     


    
    
def main():
    originalFile = "ojala.txt"
    dict = "tiny.dic"
    tinyDic = Translation(dict, originalFile)
    tinyDic.engorge()
    tinyDic.translate()
    tinyDic.POS()
    

  

if __name__ == "__main__":
    main()