import json
import pandas
from AppConfig import logger
import xml.etree.ElementTree as ET


class FileReader(object):

    def read_csv(self, file_name):
        try:
            df = pandas.read_csv(file_name)
            logger.debug(f"Read success from csv file {file_name=}")
            return df, None
        except Exception as ex:
            logger.error(f"Failed to read csv file with {ex=}")
            return None, ex

    def read_xml(self, file_name):
        try:
            root = ET.parse(file_name).getroot()
            logger.debug(f"Read success from xml file {file_name=}")
            return root, None
        except Exception as ex:
            logger.error(f"Failed to read csv file with {ex=}")
            return None, ex



    def read_json(self, filename):
        data = None
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
            logger.debug(f"Read success from json file {filename=}")
            return data, None
        except Exception as ex:
            logger.error(f"Failed to read json file with {ex=} ")
            return data, ex


