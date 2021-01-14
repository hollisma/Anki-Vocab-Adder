from aqt import mw
from aqt.qt import QAction
from aqt.utils import showInfo
from anki.importing import TextImporter

def testFunction(): 
  file = u"/home/hollisma/.local/share/Anki2/addons21/myaddon/cards.txt"

  # Select deck
  did = mw.col.decks.id("Vocab")
  mw.col.decks.select(did)

  # Settings for cards
  m = mw.col.models.byName("Cloze")
  deck = mw.col.decks.get(did)
  deck['mid'] = m['id']
  mw.col.decks.save(deck)
  m['did'] = did
  mw.col.models.save(m)

  # Import cards
  ti = TextImporter(mw.col, file)
  ti.initMapping()
  ti.run()

  showInfo('Done!')

# Add button in dropdown menu
action = QAction('Add vocab cards!', mw)
action.triggered.connect(testFunction)
mw.form.menuTools.addAction(action)

