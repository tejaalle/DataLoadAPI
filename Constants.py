class Constants(object):
    YAML_PATH = "config/logging.yml"
    CONFIG_PATH = "config/config.yaml"
    CUSTOMER_FILE = "customers_file"
    ITEMS_FILE = "items_file"
    TRANSACTIONS_FILE = "transactions_file"
    MEMBERSHIP_DATE = "membership_date"
    PRICE = "price"
    CATEGORY = "category"
    TRANSACTION_DATE = "transaction_date"
    CUSTOMER_ID = "customer_id"
    ITEM_ID = "item_id"
    MANIFEST_FILE = "manifest_file"
    DATE_FORMAT = "%Y-%m-%d"
    EXTENSIONS_SUPPORTED= "extensions_supported"
    TIME_TAKEN_TO_PROCESS = "time_taken_to_process"

    def __setattr__(self, key, value):
        raise TypeError("Assignment is not supported by constant variable")