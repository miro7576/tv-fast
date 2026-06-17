import requests
from flask import Flask, render_template, Response, request, stream_with_context

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# 💡 تم إصلاح الخطأ جذرياً هنا باستخدام البث المتدفق ذو السياق لمنع انهيار السيرفر
@app.route('/stream-proxy')
def stream_proxy():
    original_url = request.args.get('url')
    if not original_url:
        return "Missing URL", 400
        
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'http://asmrasmr.live'
        }
        
        # الاتصال بالسيرفر الأصلي بشكل متدفق
        req = requests.get(original_url, headers=headers, stream=True, timeout=10)
        
        # دالة داخلية لتوليد أجزاء الفيديو وتمريرها فوراً دون حجز الذاكرة
        def generate():
            for chunk in req.iter_content(chunk_size=4096):
                if chunk:
                    yield chunk

        # إرسال الاستجابة كـ Stream مستمر ومتوافق مع المتصفحات لإنهاء خطأ 500
        return Response(
            stream_with_context(generate()),
            content_type=req.headers.get('Content-Type', 'application/x-mpegURL'),
            status=req.status_code
        )
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
