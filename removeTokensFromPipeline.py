import spacy
from spacy.attrs import LOWER, POS, ENT_TYPE, IS_ALPHA
from spacy.tokens import Doc
import numpy

def remove_tokens_on_match(doc):
    indexes = []
    for index, token in enumerate(doc):
        if (token.pos_  in ('PUNCT', 'NUM', 'SYM')):
            indexes.append(index)
    np_array = doc.to_array([LOWER, POS, ENT_TYPE, IS_ALPHA])
    np_array = numpy.delete(np_array, indexes, axis = 0)
    doc2 = Doc(doc.vocab, words=[t.text for i, t in enumerate(doc) if i not in indexes])
    doc2.from_array([LOWER, POS, ENT_TYPE, IS_ALPHA], np_array)
    return doc2

# load english model
nlp  = spacy.load('en')
doc = nlp(u'This document is only an example. \
I would like to create a custom pipeline that will remove specific tokens from \
the final document.')
print(remove_tokens_on_match(doc))