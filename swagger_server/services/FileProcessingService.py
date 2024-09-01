from AppConfig import logger
from dateutil.parser import parse
import pandas as pd
from AppConfig import config
from Constants import Constants
from flask_log_request_id import current_request_id
from datetime import datetime
from Globals import globals


class FileProcessingService():
    def __init__(self, file_reader):
        self.file_reader = file_reader

    """process_data

        :param files: 
        :type files: dict | bytes
        :description: extracts data from customer, items and transactions data and perform some cleaning and creates and comprehensive dataset
        :rtype: tuple(str, Exception)
        """

    def process_data(self, files):

        try:
            output = None
            start_time = datetime.now()
            # Extracting data from files
            customers, exception = self.__read_file_to_df(files[Constants.CUSTOMER_FILE])
            if exception:
                logger.critical(f"Failed to read Customers file with {exception=}")
                return output, exception
            items, exception = self.__read_file_to_df(files[Constants.ITEMS_FILE])
            if exception:
                logger.critical(f"Failed to read items file with {exception=}")
                return output, exception

            transactions, exception = self.__read_file_to_df(files[Constants.TRANSACTIONS_FILE])
            if exception:
                logger.critical(f"Failed to read transactions file with {exception=}")
                return output, exception
            logger.info("Success reading customers, Items and Transactions")

            # Performing some transformations
            customers[Constants.MEMBERSHIP_DATE] = customers[Constants.MEMBERSHIP_DATE].apply(self.__format_date)
            transactions[Constants.TRANSACTION_DATE] = transactions[Constants.TRANSACTION_DATE].apply(
                self.__format_date)
            logger.info("Success formatting date columns on all datasets")
            items = items.astype({Constants.PRICE: float})
            price_category_mean = items.groupby(Constants.CATEGORY)[Constants.PRICE].mean().round(2)
            items[Constants.PRICE] = items.apply(self.__fill_dfNan_category,
                                                 args=(price_category_mean, Constants.PRICE, Constants.CATEGORY),
                                                 axis=1)
            logger.info("Success filling up null price values to category mean")
            convert_dict = {Constants.CUSTOMER_ID: int,
                            Constants.ITEM_ID: int
                            }
            transactions = transactions.astype(convert_dict)

            # Merging the datasets

            comprehensive_view = pd.merge(pd.merge(transactions, customers, on=Constants.CUSTOMER_ID), items,
                                          on=Constants.ITEM_ID)
            current_id = current_request_id()
            id = current_id[-10:-1]
            output_file_name = "output/output_file_" + id
            manifest_file_name = "manifest/manifest_file_"+id+".txt"
            row_count = comprehensive_view.shape[0]
            logger.info(f"Success creating the comprehensive_view with {row_count=}")

            # Outputing the datasets
            with open(manifest_file_name, "w") as m:
                for customer_id in comprehensive_view[Constants.CUSTOMER_ID].unique():
                    customer_info = "custId_"+ str(customer_id)
                    curr_output_file_name = output_file_name+"_"+ customer_info
                    with open(curr_output_file_name, "w") as f:
                        customer_df = comprehensive_view[comprehensive_view[Constants.CUSTOMER_ID]==customer_id]
                        f.write(customer_df.to_json(orient='records', lines=True, force_ascii=False))
                        f.close()
                        m.write(f"{customer_info}:  {customer_df.shape[0]}\n")
                m.close()
            logger.info(f"Success creating Jsonl files and adding it to manifest file")
            end_time = datetime.now()
            time_diff = end_time - start_time

            # Monitoring
            self.__observe_time_taken(manifest_file_name, time_diff.seconds)
            logger.info(f"Added time taken to process {manifest_file_name} to prometheus {time_diff.seconds} ")
            return manifest_file_name, None
        except Exception as ex:
            logger.critical(f"Exception occurred while processing the files. Failed with exception {ex=} ")
            return None, ex

    def __format_date(self, date_str):
        parsed_date = parse(date_str)
        return parsed_date.strftime(Constants.DATE_FORMAT)

    def __xml_to_dictList(self, xmlRoot):
        #Parses the xml root element into list of dictonaries
        rootList = []
        for items in xmlRoot:
            itemDict = {}
            for item in items:
                itemDict[item.tag] = item.text
            rootList.append(itemDict)
        return rootList

    def __fill_dfNan_category(self, row, category_map, update_column, category_column):
        if (pd.isnull(row[update_column])):
            return category_map[row[category_column]]
        else:
            return row[update_column]

    def __dict_to_df(self, dict):
        return pd.DataFrame(dict)

    def is_file_format_supported(self, file_name):
        # return boolean value checking if the file extension is currently supported by us
        try:
            extension_list = file_name.rsplit(".", 1)
            if extension_list[-1] in config[Constants.EXTENSIONS_SUPPORTED]:
                return True, None
            else:
                return False, None
        except Exception as ex:
            return None, ex

    def get_file_extension(self, file_name):
        # Returns the file extension
        try:
            extension_list = file_name.rsplit(".", 1)
            return extension_list[-1], None
        except Exception as ex:
            return None, ex

    """__read_file_to_df

            :param file_name: 
            :type file_name: str 
            :description: checks if the file is in supported format and then tries to load to a DataFrame
            :rtype: tuple(DatFrame, Exception)
            """

    def __read_file_to_df(self, file_name):
        try:
            extension, exception = self.get_file_extension(file_name)
            if exception:
                logger.error(f"Error while getting file extension for {file_name=}")
                return None, exception
            output_Df = None
            if extension == "json":
                data, exception = self.file_reader.read_json(file_name)
                if exception:
                    logger.error(f"Exception occurred while reading json file {file_name=} {exception=}")
                    return output_Df, exception
                output_Df = self.__dict_to_df(data)
            elif extension == "csv":
                data, exception = self.file_reader.read_csv(file_name)
                if exception:
                    logger.error(f"Exception occurred while reading csv file {file_name=} {exception=}")
                    return output_Df, exception
                output_Df = data
            elif extension == "xml":
                data, exception = self.file_reader.read_xml("transactions.xml")
                if exception:
                    logger.error(f"Exception occurred while reading xml file {file_name=} {exception=}")
                    return output_Df, exception
                data_list = self.__xml_to_dictList(data)
                output_Df = self.__dict_to_df(data_list)
            return output_Df, None
        except Exception as ex:
            logger.error(f"Exception occurred while reading file to dataframe {file_name=} {ex=}")
            return None, ex

    def __observe_time_taken(self, output_file_name, time_diff):
        time_taken_to_process = globals.get(Constants.TIME_TAKEN_TO_PROCESS)
        time_taken_to_process.labels(output_file_name=output_file_name).observe(time_diff)
