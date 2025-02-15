from flask import Flask, request, jsonify, send_file, abort
import os
from flask_cors import CORS

app = Flask(__name__)
# 启用 CORS，允许所有域名访问
CORS(app)

app.config["EXPORT_DIR"] = os.path.join(os.path.dirname(__file__), "exports")

def format_repose(code=0, message='', data=None):
    return jsonify({
        'code': code,
        'message': message,
        'data': data
    })

@app.route('/')
def hello_world():
    return 'Hello Flask!'

@app.route('/department/export', methods=['POST'])
def export_department():
    print(request.get_json())

    data = {
        'downloadLink': "test.xlsx"
    }

    print(app.config.get('EXPORT_DIR'))

    return format_repose(data=data)

@app.route('/department/download/<fileName>', methods=['GET'])
def download_department(fileName):
    filePath = os.path.join(app.config.get('EXPORT_DIR'), fileName)
    # 检查文件是否存在
    if not os.path.isfile(filePath):
        abort(404, description='File not found')

    # 使用流式传输发送文件，此种方式可以应对大文件传输
    return send_file(
        filePath,
        as_attachment=True,  # 作为附件下载
        conditional=True,     # 支持条件请求（如 Range 请求）
        mimetype='application/octet-stream'  # 二进制流类型
    )

if __name__ == '__main__':
    app.run(debug=True)