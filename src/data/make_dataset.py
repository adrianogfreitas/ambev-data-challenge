# -*- coding: utf-8 -*-
"""Download the dataset and transform into a CSV File."""
import logging
import os
import pandas as pd
from pyxlsb import open_workbook
import wget

def init_log():
    """Create a log for making dataset."""
    logger = logging.getLogger('Make Dataset')
    logger.setLevel(logging.INFO)

    # create file handler
    fh = logging.FileHandler('src/data/make_dataset.log')
    fh.setLevel(logging.INFO)

    # create console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger
    

def check_download(url, raw_path, filename, logger):
    """Check if the raw file exists and download if necessary.

    Args:
        url: url for download
        raw_path: path to store raw files
        filename: name of the file to be stored after downloaded

    """
    raw_file = os.path.join(raw_path, filename)
    logger.info('Checking file: {}'.format(raw_file))
    if os.path.isfile(raw_file):
        logger.info('- File exists!')
        return
        
    logger.info('- Downloading file...')
    wget.download(url, raw_file)
    logger.info('- Downloaded.')
    return

def save_to_csv(raw_path, filename, logger):
    """Convert the xlsb file into csv. Generates one csv per sheet.

    Args:
        raw_path: path where xlsb is stored in
        filename: name of the xlsb file

    """
    raw_file = os.path.join(raw_path, filename)
    base_csv_file = raw_file.replace('.xlsb', '').replace('/raw', '/interim')

    logger.info('Opening file: {}'.format(raw_file))
    with open_workbook(raw_file) as wb:
        for sheetname in wb.sheets:
            logger.info('- Working on sheet: {}'.format(sheetname))
            csv_file = '{}_{}.csv'.format(base_csv_file, sheetname)
            if os.path.isfile(csv_file):
                logger.info('- Sheet already converted: {}'.format(csv_file))
                continue

            df = []
            logger.info('- Reading data...')
            with wb.get_sheet(sheetname) as sheet:
                for i, row in enumerate(sheet.rows()):
                    values = [r.v for r in row]
                    df.append(values)
                    if i % 1000 == 0:
                        logger.info('{:6d} loaded rows...'.format(i))
            
            logger.info('- Converting')
            df = pd.DataFrame(df[1:], columns=df[0])
            logger.info('- Creating a file: {}'.format(csv_file))
            df.to_csv(csv_file, index=False)
            logger.info('- Done!')


if __name__ == '__main__':
    url = 'https://s3.amazonaws.com/video.udacity-data.com/topher/2018/October/5bbfaf8a_ambev-final-dataset/ambev-final-dataset.xlsb'
    filename = 'ambev-final-dataset.xlsb'
    raw_path = 'data/raw/'

    logger = init_log()
    check_download(url, raw_path, filename, logger)
    save_to_csv(raw_path, filename, logger)
