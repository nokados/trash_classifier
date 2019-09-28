import matplotlib
matplotlib.use('Agg')

from flask import Flask, request, jsonify
from fastai.vision import *
from pathlib import Path
import os
from PIL import Image

from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploaded'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

app.config.from_object(__name__)

dest_path = 'resized'
if not os.path.exists(dest_path):
    os.makedirs(dest_path)
WIDTH = 512; HEIGHT = 384


path = Path(os.getcwd())
learn = load_learner(path, 'trashclf.pkl')


@app.route('/', methods=['POST'])
def analyze_trash_photo():
    if 'file' not in request.files:
        return 'No file part: ' + ', '.join(request.files.keys()) 
    file = request.files['file']
    new_path = prepare_image(file.stream, file.filename)
    myimg = open_image(new_path)
    pred = learn.predict(myimg)
    cat_text = pred[0].obj
    cat = int(pred[1])
    prob = float(pred[2][cat])
    return jsonify({'category': cat_text, 'probability': prob})

def prepare_image(image_path, name):
    pic = Image.open(image_path)
    pic = pic.convert("RGB")

    w, h = pic.size
    new_h = int(max(HEIGHT, h * WIDTH/w))
    pic = pic.resize((WIDTH, new_h))
    pic = pic.crop((0, (new_h-HEIGHT)//2, WIDTH, (new_h-HEIGHT)//2 + HEIGHT))
    save_path = os.path.join(dest_path, name)
    pic.save(save_path)
    return save_path

if __name__ == '__main__':
    app.run(host= '0.0.0.0')