from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
from io import BytesIO
from PIL import Image, ImageDraw


def recognize_text(subscription_key, endpoint, uploaded_file):
    # Create a ComputerVisionClient object
    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
    
    # Read the image from the BytesIO object
    image_data = BytesIO(uploaded_file.read())
    
    # Call the Read API with the image data and raw response
    read_response = computervision_client.read_in_stream(image_data, raw=True)

    # Get the operation location (URL with an ID at the end) from the response
    read_operation_location = read_response.headers["Operation-Location"]
    # Grab the ID from the URL
    operation_id = read_operation_location.split("/")[-1]

    # Call the "GET" API and wait for it to retrieve the results 
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in ['notStarted', 'running']:
            break
        # time.sleep(1)

    # Print the detected text, line by line
    text = ""
    lines = []
    bounding_boxes = []
    if read_result.status == OperationStatusCodes.succeeded:
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                text += line.text + '\n'
                lines.append(line.text)
                bounding_boxes.append(line.bounding_box)

    return text, lines, bounding_boxes

def plot_bounding_boxs(bounding_boxes, image, thickness=5):
    for bounding_box in bounding_boxes:
        start_point = bounding_box[:2]
        start_point = [int(x) for x in start_point]
        end_point = bounding_box[4:6]
        end_point = [int(x) for x in end_point]
        bbox = start_point + end_point
        draw = ImageDraw.Draw(image)
        draw.rectangle(bbox, outline="green")
    return image
