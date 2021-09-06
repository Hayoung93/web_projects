import os
import json

from flask import Flask, request, render_template, Markup, redirect, url_for
from flask_cors import CORS
from base64 import b64encode


app = Flask(__name__, template_folder='/workspace/denoise_server', static_folder="/")
CORS(app)

@app.route("/", methods=["GET", "POST"])
def index():
    return redirect(url_for("show_template"))

@app.route('/denoise', methods=['GET', 'POST'])
def show_template():
    
    if "image" in request.files:
        input_image = request.files["image"]
        input_image.save(input_image.filename)
        input_image = os.path.join('/workspace/denoise_server', input_image.filename)
        # print(input_image)
    else:
        input_image = "/data/temp/DrCho_NR/noisy_depth.bmp"
    
    user_image, result_info = remove_noise(input_image)
    result_info = json.dumps(result_info)
    # result_info = Markup("<br/>".join(result_info.replace("{", "").replace("}", "").split(",")))
    result_info = result_info.replace("{", "").replace("}", "").split(",")
    print(result_info)

    return render_template(
                'template.html',
                user_image=user_image,
                input_image=input_image,
                result_info=result_info
            )


def remove_noise(input_image_path):
    # ----Will be replaced by a function call which processes input image
    output_image_path = '/data/temp/DrCho_NR/Self2Self-20000_depth_eh.bmp'
    result_info = {"noise_level": 5, "process_time": 0.489}
    # ----

    return output_image_path, result_info


if __name__ == "__main__":
    app.debug = True
    # app.config['UPLOAD_FOLDER'] = '/workspace'
    app.config['MAX_CONTENT_PATH'] = 100000000
    app.run(host='0.0.0.0', port=7700, threaded=True)