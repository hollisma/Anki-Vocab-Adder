import requests
import json
import re

options = {
  'all_words': True,  # Determines if all words will be used or just one
  'word': 'judiciously',  # Which word will be used if all_words is false
  'output_file': 'cards.txt',  # Output file name
  'anki_output': True,  # Write in Anki-card format or in readable format
  'include_quotes': False  # Include quotes if short sentences are not available
}

# Get words
file = open('words.txt', 'r')
words = file.readlines()
file.close()
words = [word.strip() for word in words]

def getURL(word): 
  APIKey = 'ab1361da-bc00-4b41-a62c-9a98355f90a5'
  return 'https://www.dictionaryapi.com/api/v3/references/collegiate/json/%s?key=%s' % (word, APIKey)

# Clean the definitions and sentences
def clean(s): 
  s = s.strip()
  # bc, qword, wi, it: take out
  s = re.sub(r'{(?:bc|qword|/qword|wi|/wi|it|/it)}', '', s)
  # dx, dx_def: take out everything until /dx_def
  s = re.sub(r'\{(?:dx|dx_def)\}.*\{(?:/dx|/dx_def)\}', '', s)
  # a_link, d_link, sx, dxt: use first things after the |, or just start from the char 2 after
  s = re.sub(r'\{(?:a_link|d_link|sx|dxt)\|(.*?)\|.*\}', r'\1', s)
  s = re.sub(r' +', r' ', s)
  s = re.sub(r' : ', r': ', s)
  s = re.sub('"', '', s)
  
  return s

def getProps(res): 
  # Get root word
  root = ''
  try: 
    root = res[0]['meta']['stems'][0]
  except: 
    print('root error occurred')

  # Get PoS (noun, verb, etc.)
  pos = ''
  try: 
    switch = {
      'noun': 'n',
      'verb': 'v',
      'adjective': 'adj', 
      'adverb': 'adv'
    }
    pos = res[0]['fl']
    pos = switch[pos]
  except:  
    print('pos error occurred')

  # Get definition
  definition = ''
  try: 
    definition = res[0]['shortdef'][0]
  except: 
    print('definition error occurred')

  # Get sentence
  sentence = ''
  try: 
    sseq = json.dumps(res[0]['def'][0]['sseq'], indent=2)
    t_index = sseq.find('"t"')
    if t_index != -1: 
      t_index_end = sseq[t_index:].find('\n')
      sentence = sseq[t_index + 6:t_index + t_index_end - 1]
      return root, pos, clean(definition), clean(sentence)

    sseq = json.dumps(res[1]['def'][0]['sseq'], indent=2)
    t_index = sseq.find('"t"')
    if t_index != -1: 
      t_index_end = sseq[t_index:].find('\n')
      sentence = sseq[t_index + 6:t_index + t_index_end - 1]
      return root, pos, clean(definition), clean(sentence)

    raise
  except: 
    if options['include_quotes']: 
      try: 
        sentence = res[0]['quotes'][0]['t']
      except: 
        try: 
          sentence = res[0]['quotes'][0]['t']
        except: 
          print('sentence error occurred')
    else: 
      print('sentence error occurred')
  
  return root, pos, clean(definition), clean(sentence)


output = open(options['output_file'], 'w')

if options['all_words']: 
  sentence_errors = []
  definition_errors = []
  for word in words: 

    # Make req to dictionary API
    endpoint = getURL(word)
    res = requests.get(endpoint).json()
    root, pos, definition, sentence = getProps(res)
    
    # Check for errors
    if definition == '': 
      definition_errors.append(word)
    if sentence == '': 
      sentence_errors.append(word)

    # Write to file
    if options['anki_output']: 
      if sentence: 
        output.write('"{{c1::%s}} (%s) {{c2::%s}}";"\n%s"\n' % (root, pos, definition, sentence))
      else: 
        output.write('"{{c1::%s}} (%s) {{c2::%s}}"\n' % (root, pos, definition))
    else: 
      output.write('%s (%s) %s\n\t%s \n' % (root, pos, definition, sentence))

  # Print words with errors
  print('definition errors:', definition_errors)
  print('sentence errors:', sentence_errors)
else: 

  # Write the json response to the output file
  word = options['word']
  endpoint = getURL(word)
  res = requests.get(endpoint).json()
  root, pos, definition, sentence = getProps(res)
  print('"{{c1::%s}} (%s) {{c2::%s}}";\\n%s\n' % (root, pos, definition, sentence))
  print(root, pos, definition, ';', sentence)
  parsed = json.dumps(res, indent=2)
  output.write(parsed)




