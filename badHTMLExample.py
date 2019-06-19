import spacy
from spacy.matcher import Matcher
from spacy.tokens import Token

# we're using a class because the component needs to be initialised with
# the shared vocab via the nlp object
class BadHTMLMerger(object):
    def __init__(self, nlp):
        # register a new token extension to flag bad HTML
        Token.set_extension('bad_html', default=False, force=True)
        self.matcher = Matcher(nlp.vocab)
        self.matcher.add('BAD_HTML', None,
            [{'ORTH': '<'}, {'LOWER': 'br'}, {'ORTH': '>'}],
            [{'ORTH': '<'}, {'LOWER': 'br/'}, {'ORTH': '>'}])

    def __call__(self, doc):
        # this method is invoked when the component is called on a Doc
        matches = self.matcher(doc)
        spans = []  # collect the matched spans here
        for match_id, start, end in matches:
            spans.append(doc[start:end])
        for span in spans:
            span.merge()   # merge
            for token in span:
                token._.bad_html = True  # mark token as bad HTML
                doc.vocab[token.text].is_stop = True  # mark lexeme as stop word
        return doc

nlp = spacy.load('en_core_web_sm')
html_merger = BadHTMLMerger(nlp)
nlp.add_pipe(html_merger, last=True)  # add component to the pipeline
doc = nlp(u"Hello<br>world! <br/> This <br> is a test.")
for token in doc:
    if token._.bad_html != True:
        print(token.text)