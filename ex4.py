import logging
from typing import List, Any
import copy
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


class TripleRes:

    def __init__(self):
        self.subject = list()
        self.relation = list()
        self.object = list()
        self.is_verb_exist = False
        self.last_pos_propn = False
        self.to_init = False

    def __repr__(self):
        return "{Subject: " + str(self.subject) + ", Relation: " + str(self.relation) + ", Object: " + str(
            self.object) + "}"

    def is_valid(self):
        return len(self.subject) > 0 and len(self.relation) > 0 and len(self.object) > 0 and self.is_verb_exist

    def add_propn(self, word):
        self.last_pos_propn = True
        if len(self.relation) == 0:
            self.subject.append(word)
        else:
            self.object.append(word)
        if  len(self.subject) > 0 and  len(self.object) > 0 and  not self.is_verb_exist:
            self.to_init = True


    def add_verb_or_adp(self, word):
        self.last_pos_propn = False
        if len(self.subject) > 0 and len(self.object) == 0:
            if word.pos_ == VERB:
                self.is_verb_exist = True
            self.relation.append(word)


def get_result_for_page(wiki_page):
    nlp_model = spacy.load('en')
    analyzed_wiki_page = nlp_model(wiki_page)
    logger.info(f"\nOriginal text analyzed:\n")
    logger.info(([(w.text, w.pos_) for w in analyzed_wiki_page]))
    pos_base_consecutive = find_consecutive_nouns_pairs(analyzed_wiki_page)
    dep_tree_base_consecutive = find_consecutive_pairs_dependency_tree(
        find_heads_sets(find_propn_heads(analyzed_wiki_page)))
    logger.info(f"Triple num for POS base extractor is : {len(pos_base_consecutive)}")
    logger.info(f"Triple num for dependency trees base extractor is : {len(dep_tree_base_consecutive)}")

    logger.info(f"\nFull result of POS base are:\n")
    logger.info(pos_base_consecutive)
    logger.info(f"\nFull result of dependency trees are:\n")
    logger.info(dep_tree_base_consecutive)




def find_propn_heads(analyzed_page: tokens.doc.Doc) -> list:
    heads = list()
    for word in analyzed_page:

        if word.pos_ == PROPN and word.dep_ != COMPOUND:
            heads.append(word)
    return heads


def find_heads_sets(heads: list) -> dict:
    heads_sets = dict()
    for h in heads:
        heads_sets[h] = set()
        heads_sets[h].add(h)
        for child in h.children:
            if child.dep_ == COMPOUND:
                heads_sets[h].add(child)
    return heads_sets


def find_consecutive_pairs_dependency_tree(heads_sets_dict: dict) -> list:
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
    curr_triple = TripleRes()

    for word in analyzed_page:
        current_pos = word.pos_
        if curr_triple.last_pos_propn and curr_triple.is_valid() and current_pos != PROPN:
            proper_nouns_pairs.append(curr_triple)
            old_triple_object = copy.copy(curr_triple.object)
            curr_triple = TripleRes()
            curr_triple.subject = old_triple_object
        if current_pos == PROPN:
            curr_triple.add_propn(word)
            if curr_triple.to_init:
                curr_triple = TripleRes()
                curr_triple.add_propn(word)
        elif current_pos in [VERB, ADP]:
            curr_triple.add_verb_or_adp(word)
        elif current_pos == PUNCT:
            if curr_triple.is_valid():
                proper_nouns_pairs.append(curr_triple)
            curr_triple = TripleRes()
        else:
            curr_triple.last_pos_propn = False



    return proper_nouns_pairs


def test_S():
    t = TripleRes()
    t.object.append("o")
    t.relation.append("r")
    t.subject.append("s")
    t.subject.append("s2")
    k = list()
    k.append(t)
    k.append(t)
    print(1 == 2 or 3)


if __name__ == '__main__':
    # test_S()
    main()
