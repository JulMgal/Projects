import sys
import os
sys.path.append('../')
import logging
from client.client.common.variables import LOGGING_LEVEL

client_formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')
path = os.getcwd()
path = os.path.join(path, 'client.log')
steam = logging.StreamHandler(sys.stderr)
steam.setFormatter(client_formatter)
steam.setLevel(logging.INFO)
log_file = logging.FileHandler(path, encoding='utf8')
log_file.setFormatter(client_formatter)
logger = logging.getLogger('client')
logger.addHandler(steam)
logger.addHandler(log_file)
logger.setLevel(LOGGING_LEVEL)

if __name__ == '__main__':
    logger.critical('Test critical event')
    logger.error('Test error ivent')
    logger.debug('Test debug ivent')
    logger.info('Test info ivent')
