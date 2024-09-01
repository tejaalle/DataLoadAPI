import connexion

from AppConfig import config, logger
from FileReader import FileReader
from swagger_server.models.process_data_error import ProcessDataError
from swagger_server.models.process_data_input import ProcessDataInput
from swagger_server.models.process_data_output import ProcessDataOutput
from swagger_server.services.FileProcessingService import FileProcessingService


def process_data(body=None):  # noqa: E501
    """process_data

    :param body: 
    :type body: dict | bytes

    :rtype: ProcessDataOutput
    """
    if connexion.request.is_json:
        logger.debug("process_data_controller started processing files")
        body = ProcessDataInput.from_dict(connexion.request.get_json())  # noqa: E501
        file_reader = FileReader()
        fileProcessingService = FileProcessingService(file_reader)
        files = {"customers_file": body.customers_file, "items_file": body.items_file, "transactions_file": body.transactions_file}

        #checks if the input has the file_name and is in supported formart.  if fileName not provided, loads the default filename from config
        for file in files:
            if files[file]:
                supported, exception = fileProcessingService.is_file_format_supported(files[file])
                if exception:
                    logger.critical(f"Failed while checking the file format with {exception=}")
                    return ProcessDataError("PDP500", f"Failed while checking the file format with {exception=}"), 500
                if not supported:
                    logger.error("Cannot process customer_file as we currently dont support such file format")
                    return ProcessDataError("PDP400", "Cannot process customer_file as we currently dont support such file format"), 400
            else:
                files[file] = config[file]
        logger.info("Initial Validation of file types is Done. Started processing data..")
        try:
            response, exception = fileProcessingService.process_data(files)
            if exception:
                logger.critical(f"Processing files Failed with {exception=}")
                return ProcessDataError("PDP500", f"{exception}"), 500
            logger.info("Successfully process files. Returning output")
            return ProcessDataOutput(response), 200
        except Exception as ex:
            return ProcessDataError("PDP500", f"Exception occured while processing data {ex=}")
    else:
        return ProcessDataError("PDP400", "Bad Request")

