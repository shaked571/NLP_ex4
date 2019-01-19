import logging
import wikipedia
import spacy
import datetime
from spacy import tokens
from itertools import permutations

ADP = 'ADP'

PREPOSOTIONAL_OBJ = 'pobj'

PREPOSITION = 'prep'

DIRECT_OBJECT = "dobj"

NOMINAL_SUBJECT = 'nsubj'
PUNCT = "PUNCT"
PROPN = "PROPN"
VERB = "VERB"
COMPOUND = "compound"


time = datetime.datetime.now()
logging.basicConfig(filename=f"logs\\ex4_{time.strftime('%d_%H_%M_%S')}.log", level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('myLogger')


def main():
    nlp_model = spacy.load('en')
    donald_trump_page = wikipedia.page('Donald Trump').content
    ruth_bader_page = wikipedia.page('Ruth Bader Ginsburg').content
    j_k_rowling_page = wikipedia.page('J. K. Rowling').content




    analyzed_ruth_bader_page = nlp_model(ruth_bader_page)
    analyzed_j_k_rowling_page = nlp_model(j_k_rowling_page)
    get_result_for_page(donald_trump_page, nlp_model)

    # logger.info(([(w.text, w.pos_) for w in doc4]))
    # logger.info(find_consecutive_nouns_pairs(doc4))
    # logger.info(([(w.text, w.pos_) for w in doc5]))
    # logger.info(find_consecutive_nouns_pairs(doc5))
    # logger.info(f"the type is: {type(analyzed_page)}")
    # consecutive_propn = find_consecutive_propn(analyzed_page)
    # print(consecutive_propn)
    # example = "John Jerome Smith likes Mary"
    # model = nlp_model(example)
    # heads = find_propn_heads(doc2)
    # logger.info(doc2)
    # logger.info([(w.text, w.pos_) for w in doc2])
    # logger.info(find_heads_sets(heads))
    # heads = find_propn_heads(doc)
    # logger.info(doc)
    # logger.info([(w.text, w.pos_) for w in doc])
    # logger.info(find_heads_sets(heads))


def get_result_for_page(wiki_page, nlp_model):
    analyzed_wiki_page = nlp_model(wiki_page)
    logger.info(([(w.text, w.pos_) for w in analyzed_wiki_page]))
    consecutive = find_consecutive_nouns_pairs(analyzed_wiki_page)
    logger.info(find_consecutive_nouns_pairs(analyzed_wiki_page))


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


def find_propn_heads(analyzed_page: tokens.doc.Doc) -> list:
    heads = list()
    for word in analyzed_page:

        if word.pos_ == PROPN and word.dep_ != COMPOUND:
            heads.append(word)
    return heads


def find_heads_sets(heads: list) ->dict:
    heads_sets = dict()
    for h in heads:
        heads_sets[h] = set()
        heads_sets[h].add(h)
        for child in h.children:
            if child.dep_ == COMPOUND:
                heads_sets[h].add(child)
    return heads_sets


def find_consecutive_nouns_pairs_dependency_tree(heads_sets: dict)->list:
    triples = list()
    for h1, h2 in permutations(heads_sets):
        if h1.dep_ == NOMINAL_SUBJECT:
            if h1.head == h2.head and h2.dep_ == DIRECT_OBJECT:
                triples.append((h1, set(h1.head), h2))
            elif h1.head == h2.head.head and h2.head.dep_ == PREPOSITION and h2.dep_ == PREPOSOTIONAL_OBJ:
                concat = set(h1.head)
                concat.add(h2.head)
                triples.append((h1, concat, h2))
    return triples


def find_consecutive_nouns_pairs(analyzed_page: tokens.doc.Doc) -> list:
    proper_nouns_pairs = list()
    candidate_words = list()
    is_verb_exist = False
    relation_words = set()
    for word in analyzed_page:
        current_pos = word.pos_
        if current_pos == PROPN:
            if len(candidate_words) > 0 and is_verb_exist:
                proper_nouns_pairs.append((candidate_words, relation_words, word))
                is_verb_exist = False
                candidate_words = list()
            candidate_words.append(word)
            relation_words = set()
        elif current_pos == PUNCT:
            candidate_words = list()
            is_verb_exist = False
            relation_words = set()
        elif current_pos == VERB:
            relation_words.add(word)
            is_verb_exist = True
        elif current_pos == ADP:
            relation_words.add(word)
        else:
            continue
    return proper_nouns_pairs


if __name__ == '__main__':
    main()
