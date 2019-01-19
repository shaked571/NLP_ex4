import logging
import wikipedia
import spacy
import datetime
from spacy import tokens
from itertools import permutations

time = datetime.datetime.now()

ADP = 'ADP'

PREPOSOTIONAL_OBJ = 'pobj'
PREPOSITION = 'prep'
DIRECT_OBJECT = "dobj"
NOMINAL_SUBJECT = 'nsubj'
PUNCT = "PUNCT"
PROPN = "PROPN"
VERB = "VERB"
COMPOUND = "compound"

logger = logging.getLogger('myLogger')
logger.setLevel(logging.INFO)

fh = logging.FileHandler(filename=f"logs\\ex4_{time.strftime('%d_%H_%M_%S')}.log", mode="w", encoding="utf-8")
logger.addHandler(fh)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def main():
    donald_trump_page = wikipedia.page('Donald Trump').content
    ruth_bader_page = wikipedia.page('Ruth Bader Ginsburg').content
    j_k_rowling_page = wikipedia.page('J. K. Rowling').content

    logger.info("-----------------------------------------------------------------------------------------------------")
    logger.info('Donald Trump')
    get_result_for_page(donald_trump_page)
    logger.info("-----------------------------------------------------------------------------------------------------")
    logger.info('Ruth Bader Ginsburg')
    get_result_for_page(ruth_bader_page)
    logger.info("-----------------------------------------------------------------------------------------------------")
    logger.info('J. K. Rowling')
    get_result_for_page(j_k_rowling_page)


def get_result_for_page(wiki_page):
    nlp_model = spacy.load('en')
    analyzed_wiki_page = nlp_model(wiki_page)
    logger.info(f"\nOriginal text analyzed:\n")
    logger.info(([(w.text, w.pos_) for w in analyzed_wiki_page]))
    pos_base_consecutive = find_consecutive_nouns_pairs(analyzed_wiki_page)
    dep_tree_base_consecutive = find_consecutive_pairs_dependency_tree(find_heads_sets(find_propn_heads(analyzed_wiki_page)))
    logger.info(f"Triple num for POS base extractor is : {len(pos_base_consecutive)}")
    logger.info(f"Triple num for dependency trees base extractor is : {len(dep_tree_base_consecutive)}")

    logger.info(f"\nFull result of POS base are:\n")
    logger.info(pos_base_consecutive)
    logger.info(f"\nFull result of dependency trees are:\n")
    logger.info(dep_tree_base_consecutive)


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


def find_consecutive_pairs_dependency_tree(heads_sets_dict: dict)->list:
    triples = list()
    for h1, h2 in permutations(heads_sets_dict, 2):
        if h1.dep_ == NOMINAL_SUBJECT:
            if h1.head == h2.head and h2.dep_ == DIRECT_OBJECT:
                triples.append((h1, [h1.head], h2))
            elif h1.head == h2.head.head and h2.head.dep_ == PREPOSITION and h2.dep_ == PREPOSOTIONAL_OBJ:
                concat = [h1.head, h2.head]
                triples.append((h1, concat, h2))
            else:
                continue
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

def test_S():
    heads_sets_dict = {"s":[1,2,3], "dd":[4,5,6]}
    for h, h2 in permutations(heads_sets_dict):
        print(h)
        print(h2)

if __name__ == '__main__':
    # test_S()
    main()
