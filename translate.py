import collections, nltk, string

SENTENCES_FILE = "sentences.txt"
DICT_FILE = "dict.txt"

def init_dict():
  e_f_dict = collections.defaultdict(lambda: 0)
  with open(DICT_FILE) as dict_file:
    for line in dict_file:
      word_and_def = line.split("\t")
      e_f_dict[word_and_def[0]] = word_and_def[1]
  return e_f_dict
      
def apply_rules(pos_tags):
  #RULE 1: (Noun, Adj|Adv) -> (Adj|Adv, Noun)
  for i in range(1, len(pos_tags)):
    if (pos_tags[i][1] == "JJ" or pos_tags[i][1] == "RB") and (pos_tags[i-1][1] == "NN" or pos_tags[i-1][1] == "NNS" or pos_tags[i-1][1] == "NNP"):
      pos_tags[i], pos_tags[i-1] = pos_tags[i-1], pos_tags[i]

  #RULE 2: (you) -> (your)
  for i in range(0, len(pos_tags)-1):
    if pos_tags[i][1] == "PRP" and "VB" not in pos_tags[i+1][1] and "DT" not in pos_tags[i+1][1]:
      if pos_tags[i][0] == "you":
        pos_tags[i] = ("your", pos_tags[i][1])
      if pos_tags[i][0] == "he":
        pos_tags[i] = ("his", pos_tags[i][1])
      if pos_tags[i][0] == "she":
        pos_tags[i] = ("her", pos_tags[i][1])
      if pos_tags[i][0] == "I":
        pos_tags[i] = ("my", pos_tags[i][1])
      if pos_tags[i][0] == "they":
        pos_tags[i] = ("their", pos_tags[i][1])

  #RULE 3: (no) -> (don't)
  for i in range(1, len(pos_tags)-1):
    if (pos_tags[i-1][1] == "PRP" or "NN" in pos_tags[i-1][1]) and pos_tags[i][0] == "no":
      pos_tags[i] = ("don't", pos_tags[i][1])
  
  #RULE 4: (noun of noun) -> (noun's noun)
  for i in range(1, len(pos_tags)-1):
    if "NN" in pos_tags[i+1][1] and "NN" in pos_tags[i-1][1] and pos_tags[i][0] == "of":
      next_i_minus_1 = (pos_tags[i+1][0]+"'s", pos_tags[i+1][1])
      pos_tags[i+1] = (pos_tags[i-1][0], pos_tags[i-1][1])
      pos_tags[i-1] = next_i_minus_1
      pos_tags[i] = ("", "")
      
  #Rule 5:(indirect object, verb) -> (verb, indirect object)
    #RULE 1: (Noun, Adj|Adv) -> (Adj|Adv, Noun)
  for i in range(1, len(pos_tags)):
    if (pos_tags[i][1] == "VBD") and (pos_tags[i-1][1] == "PRP"):
      pos_tags[i], pos_tags[i-1] = pos_tags[i-1], pos_tags[i]
  
  #Rule 6: If there are two nouns in a row and one of them is proper, 
  # the proper noun should come first: NNP before NNS
  for i in range(1, len(pos_tags)):
    if (pos_tags[i][1] == "NNP") and ((pos_tags[i-1][1] == "NNS") or (pos_tags[i-1][1] == "NN")):
      pos_tags[i], pos_tags[i-1] = pos_tags[i-1], pos_tags[i]
 
  #Rule 7: how/want verb -> how/want to verb
  for i in range(1, len(pos_tags)):
    if (pos_tags[i-1][1] == "WRB" or pos_tags[i-1][0] == "how" or pos_tags[i-1][0] == "want") and "VB" in pos_tags[i][1] and pos_tags[i-1][0] != "are" and pos_tags[i-1][0] != "is":
      pos_tags[i] = ("to " + pos_tags[i][0], "VB")
  
  #Rule 8: have 'special word' -> is 'special word'
  for i in range(1, len(pos_tags)):
    if pos_tags[i-1][0] == "have": 
      if pos_tags[i][0] == "hunger":
        pos_tags[i-1] = ("is", "IS")
        pos_tags[i] = ("hungry", "JJ")      
      elif pos_tags[i][0] == "cold":
        pos_tags[i-1] = ("is", "IS")
        pos_tags[i] = ("cold", "JJ")      
    elif pos_tags[i-1][0] == "ago":
      if pos_tags[i][0] == "heat":
        pos_tags[i-1] = ("it's", "ITS")
        pos_tags[i] = ("hot", "JJ")             
      elif pos_tags[i][0] == "cold":
        pos_tags[i-1] = ("it's", "ITS")
        pos_tags[i] = ("cold", "JJ")      
  
  
  #Rule 9: subject is -> subject am/are (possibly)
  for i in range(1, len(pos_tags)):
    if (pos_tags[i-1][1] == "PRP" or "NN" in pos_tags[i-1][1]) and  pos_tags[i][0] == "is":
      if pos_tags[i-1][1] == "NNS" or pos_tags[i-1][0] == "they":
        pos_tags[i] = ("are", "VBZ")
      if pos_tags[i-1][0] == "I":
        pos_tags[i] = ("am", "VBZ")

  #Rule 10: Remove double negatives
  for i in range(1, len(pos_tags)):
    if pos_tags[i][0] == "nothing":
      for j in range(0, min(i,8)):
        if pos_tags[i-j][0] == "didn't" or pos_tags[i-j][0] == "don't" or pos_tags[i-j][0] == "never" or pos_tags[i-j][0] == "no":
          pos_tags[i] = ("anything", "NN")
          break
  


  
  
 
  #TODO: More rules
  return pos_tags 


def translate():
  e_f_dict = init_dict()
  with open(SENTENCES_FILE) as sentences_file:
    for line in sentences_file:
      words = line.split()
      eng_sentence = ""
      for word in words:
        if word.lower().translate(None, string.punctuation) in e_f_dict:
          eng_sentence += e_f_dict[word.lower().translate(None, string.punctuation)] 
        else:
          eng_sentence += word
        eng_sentence += " "
      tokens = nltk.word_tokenize(eng_sentence)
      pos_tags = nltk.pos_tag(tokens)
      print line
      print pos_tags
      final_order = apply_rules(pos_tags)
      final = ""
      for word in final_order:
        final += word[0] + " "
      final += line[-2]
      print final

if __name__ == '__main__':
  translate() 
