import os
import logging
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

# Импорт обученной модели (см. раздел 5)
from model import predict_shape

# -----------------------------
# Настройка приложения
# -----------------------------
app = Flask(__name__)

# Папка для загруженных изображений
UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'uploads'
)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'webp'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # максимум 16 МБ на файл

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

# Создаём папку для загрузок, если её нет
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)


# -----------------------------
# Вспомогательные функции
# -----------------------------
def allowed_file(filename: str) -> bool:
    """Проверяет, что расширение файла допустимо."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# -----------------------------
# Маршруты
# -----------------------------

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

    # Сохраняем файл
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    try:
        result = predict_shape(filepath)   # dict
    except Exception as e:
        return jsonify({'error': f'Ошибка модели: {str(e)}'}), 500
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)

    return jsonify(result)  # {"shape": "Квадрат", "confidence": 0.98, ...}



# -----------------------------
# Обработчики ошибок
# -----------------------------
@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({'error': 'Файл слишком большой (максимум 16 МБ)'}), 413


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Внутренняя ошибка сервера'}), 500


# -----------------------------
# Запуск
# -----------------------------
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
