import os
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from flask import Flask, flash, request, redirect, render_template
from forms import UploadForm, CaptchaForm

# создаем экземпляр приложения
app = Flask(__name__)
# папка для сохранения загруженных файлов
UPLOAD_FOLDER = os.path.join('static', 'input_image')
# папка для сохранения обработанного изображения
OUTPUT_FOLDER = os.path.join('static', 'output_image')
# расширения файлов, которые разрешено загружать
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
# добавляем конфигурации
app.config['SECRET_KEY'] = str(os.urandom(10))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

app.config['RECAPTCHA_PUBLIC_KEY'] = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'


def change_contrast(img_0, level):
    """" Функция изменения контраста"""
    factor = (259 * (level + 255)) / (255 * (259 - level))

    def contrast(c):
        return 128 + factor * (c - 128)

    return img_0.point(contrast)


def allowed_file(filename):
    """ Функция проверки расширения файла """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    form_captcha = CaptchaForm()
    if request.method == "POST":
        if form_captcha.validate_on_submit():

            if form.validate_on_submit():
                f = form.upload.data
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], 'input_image.jpg'))
                return redirect('/input_image')
            else:
                flash('Загрузите файл с другим расширением')
            return render_template('index.html', form=form, form_captcha=form_captcha)
        else:
            flash('Подтвердите, что вы не робот')
            return render_template('index.html', form=form, form_captcha=form_captcha)
    return render_template('index.html', form=form, form_captcha=form_captcha)


@app.route('/input_image', methods=['GET'])
def display_image_1():
    input_image = os.path.join(app.config['UPLOAD_FOLDER'], 'input_image.jpg')
    # график
    img_0 = Image.open(UPLOAD_FOLDER + '/input_image.jpg')
    img_0 = np.array(img_0)
    graph = plt.figure()
    img_for_graph = np.array(img_0)
    img_flat = img_for_graph.flatten()
    plt.hist(img_flat, bins=200, range=[0, 256])
    plt.title("Number of pixels in each intensity value")
    plt.xlabel("Intensity")
    plt.ylabel("Number of pixels")
    plt.show()
    graph.savefig(os.path.join(app.config['OUTPUT_FOLDER'], 'graph.jpg'))
    output_graph = os.path.join(app.config['OUTPUT_FOLDER'], 'graph.jpg')
    return render_template("page_2.html", output_for_html=input_image,
                           graph_for_html=output_graph)


@app.route("/change_contrast", methods=['GET', 'POST'])
def display_image_2():
    if request.method == 'POST':

        number = int(request.form['num_lvl'])
        img_0 = Image.open(UPLOAD_FOLDER + '/input_image.jpg')
        fig = plt.figure()
        img_1 = change_contrast(img_0, number)  # изменение контраста
        plt.imshow(img_1)
        fig.savefig(os.path.join(app.config['OUTPUT_FOLDER'], 'output_image.jpg'))
        output_image = os.path.join(app.config['OUTPUT_FOLDER'], 'output_image.jpg')
        # график по пикселям
        graph = plt.figure()
        img_for_graph = np.array(img_1)
        img_flat = img_for_graph.flatten()
        plt.hist(img_flat, bins=200, range=[0, 256])
        plt.title("Number of pixels in each intensity value")
        plt.xlabel("Intensity")
        plt.ylabel("Number of pixels")
        plt.show()
        graph.savefig(os.path.join(app.config['OUTPUT_FOLDER'], 'graph.jpg'))
        output_graph = os.path.join(app.config['OUTPUT_FOLDER'], 'graph.jpg')
        return render_template("page_2.html", output_for_html=output_image, value_num=number,
                               graph_for_html=output_graph)
    else:
        input_image = os.path.join(app.config['UPLOAD_FOLDER'], 'intput_image.jpg')
        return render_template("page_2.html", output_for_html=input_image)
