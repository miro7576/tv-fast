from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    try:
        # قراءة ملف الواجهة وعرضه للمتصفح
        with open('index.html', 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return "<h1>خطأ: لم يتم العثور على ملف index.html</h1>", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
