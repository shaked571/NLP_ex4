import logging
import spacy

logging.basicConfig(filename='myapp.log', level=logging.INFO)
log = logging.getLogger('myLogger')


class Global:
    SourceIPAddress = ''


class IpFilter(logging.Filter):
    def filter(self, rec):
        return not Global.SourceIPAddress == '127.0.0.1'


def main():
    spacy.load('en')
    log.addFilter(IpFilter())
    log.info("work")
    Global.SourceIPAddress = '127.0.0.1'
    log.info("Dont log")
    print("ss")

if __name__ == '__main__':
    main()