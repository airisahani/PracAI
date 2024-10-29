from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
import time
import os
from dotenv import load_dotenv

load_dotenv()

endpoint = os.getenv("endpoint")
key = os.getenv("key")

credentials = CognitiveServicesCredentials(key)

client = ComputerVisionClient(
    endpoint=endpoint,
    credentials=credentials
)

def read_image(uri):
    numberOfCharsInOperationId = 36
    maxRetries = 10

    try:
        # SDK call
        rawHttpResponse = client.read(uri, language="en", raw=True)

        # Get ID from returned headers
        operationLocation = rawHttpResponse.headers["Operation-Location"]
        operationId = operationLocation.split('/')[-1]  # Extract the operation ID

        # Polling for results
        retry = 0
        while retry < maxRetries:
            result = client.get_read_result(operationId)
            if result.status.lower() not in ['notstarted', 'running']:
                break
            time.sleep(1)
            retry += 1
        
        if retry == maxRetries:
            return "max retries reached"

        if result.status == OperationStatusCodes.succeeded:
            res_text = " ".join([line.text for line in result.analyze_result.read_results[0].lines])
            return res_text
        else:
            return "error: {}".format(result.status)

    except Exception as e:
        return "An error occurred: {}".format(str(e))
