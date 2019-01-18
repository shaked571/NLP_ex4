import logging
import wikipedia
import spacy
import datetime
from spacy import tokens

PUNCT = "PUNCT"
PROPN = "PROPN"
VERB = "VERB"

time = datetime.datetime.now()
logging.basicConfig(filename=f"logs\\ex4_{time.strftime('%d_%H_%M_%S')}.log", level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('myLogger')


def main():
    nlp_model = spacy.load('en')
    page = wikipedia.page('Brad Pitt').content
    analyzed_page = nlp_model(page)
    doc = nlp_model(u"AMZN is a great company, John told this to Jerry which later went to Rafael the king. ")
    doc2 = nlp_model(u"The company Apple is better than Microsoft.")
    doc3 = nlp_model(u"AMZN is the best! Apple is OK.")
    doc4 = nlp_model(u"John! come here you.")
    doc5 = nlp_model(u"John and Mike went to MIT university.")
    logger.info(([(w.text, w.pos_) for w in doc]))
    logger.info(find_consecutive_nouns_pairs(doc))
    logger.info(([(w.text, w.pos_) for w in doc2]))
    logger.info(find_consecutive_nouns_pairs(doc2))
    logger.info(([(w.text, w.pos_) for w in doc3]))
    logger.info(find_consecutive_nouns_pairs(doc3))
    logger.info(([(w.text, w.pos_) for w in doc4]))
    logger.info(find_consecutive_nouns_pairs(doc4))
    logger.info(([(w.text, w.pos_) for w in doc5]))
    logger.info(find_consecutive_nouns_pairs(doc5))
    # logger.info(f"the type is: {type(analyzed_page)}")
    # consecutive_propn = find_consecutive_propn(analyzed_page)
    # print(consecutive_propn)


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



def find_consecutive_nouns_pairs(analyzed_page: tokens.doc.Doc) -> list:
    proper_nouns_pairs = list()
    candidate_word = None
    is_verb_exist = False
    relation_verb = None
    for word in analyzed_page:
        current_pos = word.pos_
        if current_pos == PROPN:
            if candidate_word is not None and is_verb_exist:
                proper_nouns_pairs.append((candidate_word, relation_verb,word))
            candidate_word = word
        elif current_pos == PUNCT:
            candidate_word = None
            is_verb_exist = False
        elif current_pos == VERB:
            relation_verb = word
            is_verb_exist = True
        else:
            continue
    return proper_nouns_pairs


if __name__ == '__main__':
    main()
