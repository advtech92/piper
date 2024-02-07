import logging

def setup_logging():
    logging.basicConfig(filename='piper.log', level=logging.INFO,
                        format='%(asctime)s:%(levelname)s:%(name)s: %(message)s')
    return logging.getLogger('Piper')

logger = setup_logging()
