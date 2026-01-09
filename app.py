from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
from PIL import Image
import os

# Импорт вашей модели (см. раздел 5)
from model import predict_shape

app = Flask(__name__)

# Папка для загруженных изображений
UPLOAD_FOLDER = r'C:\Users\luba0\Desktop\my_geometry_app\uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Создайте папку uploads, если её нет
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'Нет файла'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Файл не выбран'}), 400
    
    # Сохраняем загруженное изображение
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    
    # Загружаем и обрабатываем изображение
    #image = cv2.imread(filepath)
    #if image is None:
        
       # return jsonify({'error': 'Не удалось загрузить изображение'}), 400
    #print (image)    
    
    
    #image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
   # print (type(image_rgb))
    
    #print ('переведенное \n',image)
    
    # Вызываем вашу модель
    try:
        prediction = predict_shape(filepath)
       
    except Exception as e:
        return jsonify({'error': f'Ошибка модели: {str(e)}'}), 500
    
    # Удаляем файл после обработки
    os.remove(filepath)
    
    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)