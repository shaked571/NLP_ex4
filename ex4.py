import logging
import spacy
import numpy as _nx

logging.basicConfig(filename='myapp.log', level=logging.INFO)
log = logging.getLogger('myLogger')


def main():
    nlp = spacy.load('en')
    doc = nlp(u"This is a sentence.")
    log.info([(w.text, w.pos_) for w in doc])
    _nx.AxisError(1)



if __name__ == '__main__':
    main()

