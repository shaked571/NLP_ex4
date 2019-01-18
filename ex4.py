import logging
import wikipedia
import spacy
import datetime

time = datetime.datetime.now()

logging.basicConfig(filename=f"logs\\ex4_{time.strftime('%d_%H_%M_%S')}.log", level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger('myLogger')


def main():
    nlp_model = spacy.load('en')
    page = wikipedia.page('Brad Pitt').content
    analyzed_page = nlp_model(page)
    doc = nlp_model(u"AMZN achieved a very big profit in Q3 2017, we believe it would increase in the upcoming years")
    logger.info([(w.text, w.pos_) for w in doc])


if __name__ == '__main__':
    main()
