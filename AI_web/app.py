# coding:utf-8

from flask import Flask, render_template, send_file, request, redirect, url_for, make_response, jsonify
from werkzeug.utils import secure_filename
import os
import cv2

from datetime import timedelta
from datetime import datetime
import json

from gevent import monkey
from gevent.pywsgi import WSGIServer
monkey.patch_all()

# 设置允许的文件格式
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'JPEG', 'JPG', 'PNG', 'bmp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


app = Flask(__name__)
# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)


@app.route('/', methods=['POST', 'GET'])
@app.route('/upload', methods=['POST', 'GET'])  # 添加路由
def upload():
    if request.method == 'POST':
        f = request.files['file']

        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})

        user_input = request.form.get("name")

        basepath = os.path.dirname(__file__)  # 当前文件所在路径

        current_time = datetime.now().strftime("%Y%m%d-%H%M%S")
        upload_path = os.path.join(basepath, 'static/images', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        # upload_path = os.path.join(basepath, 'static/images','test.jpg')  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)

        # 使用Opencv转换一下图片格式和名称
        short_path = 'static/images/{}.jpg'.format(current_time)
        img = cv2.imread(upload_path)
        cv2.imwrite(os.path.join(basepath, short_path), img)

        return render_template('upload_ok.html', imgurl=short_path)

    return render_template('upload.html')


@app.route('/change', methods=['POST', 'GET'])  # 添加路由
def run_model():                                # 人脸性别转换
    image_path = request.values['image_path']
    model_name = request.values['model_name']
    current_time = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_path = 'static/images/{}.jpg'.format(current_time)
    cmd = "python3 ../CycleGAN/inference.py " \
          "--model ../CycleGAN/pretrained/{}.pb " \
          "--input {} " \
          "--output {}" \
          " --image_size 256".format(model_name, image_path, output_path)
    print("运行模型")
    os.system(cmd)
    print("运行结束")
    result = {"src": output_path}
    results = json.dumps(result, ensure_ascii=False)
    rst = make_response(results)
    rst.headers['Access-Control-Allow-Origin'] = '*'
    return rst


@app.route('/sample_poem', methods=['POST', 'GET'])  # 添加路由
def run_sample():
    prime_text = request.values['prime']
    cmd = None
    if prime_text == "":
        cmd = "python2 ../AncientChinesePoemRNN/sample.py"
    else:
        cmd = "python2 ../AncientChinesePoemRNN/sample.py --prime {}".format(prime_text)
    print("运行模型")
    os.system(cmd)
    print("运行结束")

    result_txt = None
    with open("../AncientChinesePoemRNN/result.txt", 'r', encoding='utf-8') as f:  # 打开文件
        lines = f.readlines()  # 读取所有行
        result_txt = lines[-1]  # 最后一行
        print(result_txt)
    result = {"poem": result_txt}
    results = json.dumps(result, ensure_ascii=False)
    rst = make_response(results)
    rst.headers['Access-Control-Allow-Origin'] = '*'
    return rst

@app.route('/download', methods=['GET'])  # 添加路由
def download():
    def find_new_file(path):
        lists = os.listdir(path)
        # 对获取的文件根据修改时间进行排序
        lists.sort(key=lambda x: os.path.getmtime(path + '/' + x))
        file_name = lists[-1]
        file_path = os.path.join(path, lists[-1])
        return file_name, file_path

    file_name, file_path = find_new_file("stocks/files")

    return render_template('file_download.html', file_path=file_path, file_name=file_name)

@app.route("/stocks/files/<path>")
def download_stocks(path = None):
    if path is not None:
        return send_file("/usr/PY/AI_web/stocks/files/{}".format(path), as_attachment=True)

if __name__ == '__main__':
    # app.debug = True
    #app.run(host='0.0.0.0', port=80, debug=True)
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    http_server = WSGIServer(('', 80), app)
    http_server.serve_forever()