import logging
import wikipedia
import spacy
import datetime
from spacy import tokens
PROPN = "PROPN"

time = datetime.datetime.now()
logging.basicConfig(filename=f"logs\\ex4_{time.strftime('%d_%H_%M_%S')}.log", level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('myLogger')


def main():
    nlp_model = spacy.load('en')
    page = wikipedia.page('Brad Pitt').content
    analyzed_page = nlp_model(page)
    logger.info(f"the type is: {type(analyzed_page)}")
    consecutive_propn = find_consecutive_propn(analyzed_page)
    print(consecutive_propn)


def find_consecutive_propn(analyzed_page: tokens.doc.Doc) ->list:
    current_sequence = list()
    sequences = list()
    is_consecutive_sequence = False
    for word in analyzed_page:
        current_pos = word.pos_
        if current_pos == PROPN:
            if not is_consecutive_sequence:
                current_sequence = list()
            current_sequence.append(word)
            is_consecutive_sequence = True
        else:
            if is_consecutive_sequence:
                sequences.append(current_sequence)
            is_consecutive_sequence = False
    return sequences


def find_consecutive_nouns(analyzed_page: tokens.doc.Doc) ->set:
    proper_nouns_paires = set()



if __name__ == '__main__':
    main()
