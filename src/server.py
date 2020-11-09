import io
import json

from torchvision import models
import torchvision.transforms as transforms
from PIL import Image
from flask import Flask, jsonify, request

#Create the ML Inference server instance
app = Flask(__name__)
#Initialition of inference model
imagenet_class_index = json.load(open('imagenet_class_index.json'))
model = models.densenet121(pretrained=True)
model.eval()

#function:Transfrom input image bytes to tensor
#input: image bytes
#output: image tensor
def transform_image(image_bytes):
    my_transforms = transforms.Compose([transforms.Resize(255),
                                        transforms.CenterCrop(224),
                                        transforms.ToTensor(),
                                        transforms.Normalize(
                                            [0.485, 0.456, 0.406],
                                            [0.229, 0.224, 0.225])])
    image = Image.open(io.BytesIO(image_bytes))
    return my_transforms(image).unsqueeze(0)

#function: Get image prediction result
#input: image bytes
#output: classification result
def get_prediction(image_bytes):
    tensor = transform_image(image_bytes=image_bytes)
    outputs = model.forward(tensor)
    _, y_hat = outputs.max(1)
    predicted_idx = str(y_hat.item())
    return imagenet_class_index[predicted_idx]

#Perform inference request 
#input: images
#output: classification of all images
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    #Only process POST/GET request
    if request.method == 'POST' or request.method == 'GET':
        res = {}
        #Process each image in the http request
        for file in request.files.getlist('file'):
            img_bytes = file.read()
            class_id, class_name = get_prediction(image_bytes=img_bytes)
            res[file.filename] = {'class_id': class_id, 'class_name': class_name}
        return jsonify(res)
    return jsonify({'result:': 'No Image'})


#start the inferece server
if __name__ == '__main__':
    app.run(host='0.0.0.0')