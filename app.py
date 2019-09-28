import matplotlib
matplotlib.use('Agg')

from flask import Flask, request, jsonify
from fastai.vision import *
from pathlib import Path
import os
from PIL import Image

app = Flask(__name__)
app.config.from_object(__name__)

dest_path = './resized'
if not os.path.exists(dest_path):
    os.makedirs(dest_path)
WIDTH = 512; HEIGHT = 384


path = Path(os.getcwd())
learn = load_learner(path, 'trashclf.pkl')


@app.route('/', methods=['GET'])
def analyze_trash_photo():
    if request.args and 'path' in request.args:
        path = request.args.get('path')
    else:
        return "NO path have gotten"
    new_path = prepare_image(path)
    myimg = open_image(new_path)
    pred = learn.predict(myimg)
    cat_text = pred[0].obj
    cat = int(pred[1])
    prob = float(pred[2][cat])
    return jsonify({'category': cat_text, 'probability': prob})

def prepare_image(image_path):
    pic = Image.open(image_path)
    name = os.path.basename(image_path)
    w, h = pic.size
    new_h = int(max(HEIGHT, h * WIDTH/w))
    pic = pic.resize((WIDTH, new_h))
    pic = pic.crop((0, (new_h-HEIGHT)//2, WIDTH, (new_h-HEIGHT)//2 + HEIGHT))
    save_path = os.path.join(dest_path, name)
    pic.save(save_path)
    return save_path

if __name__ == '__main__':
    app.run()