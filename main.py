import connexion
from flask_log_request_id import RequestID
from prometheus_client import start_http_server, Counter, Histogram

from AppConfig import config, logger
from Constants import Constants
from swagger_server import encoder
from Globals import globals



def main():
    global app
    app = connexion.FlaskApp(__name__)
    RequestID(app.app)
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger_server/swagger/swagger.yaml')
    start_http_server(port=8000, addr="0.0.0.0")

    # initializing globals
    # records_per_output_file = Counter("Records_Per_Output_File", "Number of Records per output file", ["Output_file_name"])
    time_taken_to_process = Histogram("Time_taken_to_process",
                                      "Time taken to process all the datasets for each request ", ["output_file_name"])

    globals.init()
    globals.set(Constants.TIME_TAKEN_TO_PROCESS, time_taken_to_process)

    logger.info("starting Pepper Data Processing server")
    app.run(host="0.0.0.0", port=8080)




if __name__=="__main__":
    main()


