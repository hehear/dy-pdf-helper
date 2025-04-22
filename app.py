import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
from flask import Flask, request, send_file, render_template
import os
import subprocess
from werkzeug.utils import secure_filename
from werkzeug.exceptions import BadRequest

app = Flask(__name__, static_folder='static')

# 配置文件上传和压缩目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
COMPRESSED_FOLDER = os.path.join(BASE_DIR, 'compressed')

# 确保目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(COMPRESSED_FOLDER, exist_ok=True)

def compress_pdf(input_path, output_path, rate=None, custom_rate=None):
    logging.info(f"开始压缩: 输入路径 {input_path}, 输出路径 {output_path}")

    if custom_rate is not None:
        # 根据用户提供的参数配置动态调整参数组
        if custom_rate >= 0.9:
            # 极高质量参数
            color_res, gray_res, mono_res = 300, 300, 300
            color_conversion = "/LeaveColorUnchanged"
            downsample = "false"
            downsample_type = "/Bicubic"
        elif 0.8 <= custom_rate < 0.9:
            # 高质量参数
            color_res, gray_res, mono_res = 250, 250, 300
            color_conversion = "/LeaveColorUnchanged"
            downsample = "true"
            downsample_type = "/Bicubic"
        elif 0.7 <= custom_rate < 0.8:
            # 中高质量参数
            color_res, gray_res, mono_res = 200, 200, 250
            color_conversion = "/sRGB"
            downsample = "true"
            downsample_type = "/Bicubic"
        elif 0.6 <= custom_rate < 0.7:
            # 中质量参数
            color_res, gray_res, mono_res = 150, 150, 200
            color_conversion = "/sRGB"
            downsample = "true"
            downsample_type = "/Average"
        elif 0.5 <= custom_rate < 0.6:
            # 中低质量参数
            color_res, gray_res, mono_res = 120, 120, 150
            color_conversion = "/sRGB"
            downsample = "true"
            downsample_type = "/Average"
        else:
            # 低质量参数（30%-50%）
            color_res, gray_res, mono_res = 96, 96, 120
            color_conversion = "/sRGB"
            downsample = "true"
            downsample_type = "/Subsample"

        command = (
            f'gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 '
            f'-dColorImageResolution={color_res} '
            f'-dGrayImageResolution={gray_res} '
            f'-dMonoImageResolution={mono_res} '
            f'-dColorConversionStrategy={color_conversion} '
            f'-dDownsampleColorImages={downsample} '
            f'-dColorImageDownsampleType={downsample_type} '
            '-dNOPAUSE -dQUIET -dBATCH '
            f'-sOutputFile={output_path} {input_path}'
        )
    else:
        pdf_settings = {
            "screen": "/screen",
            "ebook": "/ebook",
            "printer": "/printer",
            "prepress": "/prepress"
        }
        pdf_setting = pdf_settings.get(rate, "/ebook")
        command = f'gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 ' \
                  f'-dPDFSETTINGS={pdf_setting} ' \
                  f'-dNOPAUSE -dQUIET -dBATCH ' \
                  f'-sOutputFile={output_path} {input_path}'

    logging.info(f"执行命令: {command}")
    try:
        subprocess.run(command, shell=True, check=True)
        logging.info(f"压缩成功: {input_path} -> {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"压缩失败: {e}")
        return False

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/compress', methods=['POST'])
def compress():
    if 'file' not in request.files:
        raise BadRequest("没有文件上传")

    file = request.files['file']
    if file.filename == '':
        raise BadRequest("未选择文件")

    filename = secure_filename(file.filename)
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(input_path)

    compression_type = request.form.get('compressionType', 'preset')
    if compression_type == 'preset':
        rate = request.form.get('rate', 'ebook')
        custom_rate = None
    else:
        rate = None
        custom_rate_str = request.form.get('customRate')
        if custom_rate_str:
            custom_rate = int(custom_rate_str)/100  # 转换为小数
        else:
            custom_rate = 0.7  # 默认70%

    output_path = os.path.join(COMPRESSED_FOLDER, f'{filename}.compressed.pdf')
    if compress_pdf(input_path, output_path, rate=rate, custom_rate=custom_rate):
        return send_file(output_path, as_attachment=True)
    else:
        raise BadRequest("压缩失败，请检查文件是否有效。")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8009, debug=False)