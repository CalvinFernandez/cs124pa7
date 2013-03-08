import collections, re, string

word_dict= collections.defaultdict(lambda: 0)
output = open("dict_copy.txt", 'w')
with open("sentences.txt") as file:
  for line in file:
    words = line.split()
    for word in words:
      word_dict[word.lower().translate(None, string.punctuation)] = 1

for word in word_dict:
  output.write(word+"\n")

output.close()
