import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

AZURE_SERVICE_BUS = {
    "ConnectionString": os.getenv("SERVICE_BUS_CONNECTION_STR"),
}

RABBIT_MQ = {
    "UserName": 'admin',
    "Password": '${1}',
    "Port": 5672,
    "VirtualHost": "/",
    "Host": '10.231.91.4'
}

QUEUE_NAMES = {
    "default_queue": "mysbqueue",
    "batch_queue": "mrraas_qa03_batch_queue",
    "ocr_queue": "mrraas_qa03_ocr_queue",
    "nlp_queue": "mrraas_qa03_nlp_queue",
    "result_queue": "mrraas_qa03_result_queue"
}