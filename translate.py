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
  #RULE 1: (Noun, Adj) -> (Adj, Noun)
  for i in range(1, len(pos_tags)):
    if (pos_tags[i][1] == "JJ") and (pos_tags[i-1][1] == "NN" or pos_tags[i-1][1] == "NNS" or pos_tags[i-1][1] == "NNP"):
      pos_tags[i], pos_tags[i-1] = pos_tags[i-1], pos_tags[i]
  
  """  
  for i in range(1, len(pos_tags)):
    if (pos_tags[i][1] == "JJ") and (pos_tags[i-1][1] == "NN" or pos_tags[i-1][1] == "NNS" or pos_tags[i-1][1] == "NNP"):
      pos_tags[i], pos_tags[i-1] = pos_tags[i-1], pos_tags[i]
  """
 
  #RULE 2: (you) -> (your)
  for i in range(0, len(pos_tags)-1):
    if pos_tags[i][1] == "PRP" and "VR" not in pos_tags[i+1][1] and "DT" not in pos_tags[i+1][1]:
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
