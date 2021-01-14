# Vocab Adder
Ever see unfamiliar words and want to put them into Anki without having to manually search up definitions? Vocab Adder does just that by creating Anki vocab cards out of a list of words. 

# Instructions
* Move this folder into the Anki addons folder (to locate, goto Tools > Addons > View Files)
* Add the words you want to learn to words.txt, with each word on its own line
* Run 'python vocab_script.py' to create the Anki-ready cards.txt
* Go into Anki and create a root deck called 'Vocab'
* Under Tools, click 'Add vocab cards!' and the cards will be added to the root Vocab deck

Note: in order to make calls to the dictionary API, you'll need to create a developer account at https://dictionaryapi.com/[https://dictionaryapi.com/] and use the API key in the getURL() method in vocab_script.py. 