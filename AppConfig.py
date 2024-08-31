import logging.config
import os.path
import yaml

from Constants import Constants
class AppConfig(object):
    logger_path = Constants.YAML_PATH
    logger = None
    config_path = Constants.CONFIG_PATH
    config = None
    def __init__(self):
        self.logger = self.create_logger(self.logger_path)
        self.config = self.load_config(self.config_path)

    def create_logger(self, file_path):
        try:
            with open(os.path.join(os.path.dirname(__file__), file_path), "r", encoding="utf-8") as log_config:
                loaded_log_config = yaml.load(log_config, Loader=yaml.FullLoader)
                logging.config.dictConfig(loaded_log_config)
            return logging.getLogger()
        except Exception as ex:
            raise ex

    def load_config(self, file_path):
        try:
            with open(os.path.join(os.path.dirname(__file__), file_path), "r", encoding="utf-8") as config_file:
                return yaml.safe_load(config_file)
        except Exception as ex:
            raise ex




appConfig = AppConfig()
logger = appConfig.logger
config = appConfig.config
