from flask import Flask, Response
import requests

app = Flask(__name__)

# بيانات حسابك الصحيحة
HOST = "http://live.lynxiptv.xyz:80"
USER = "777685932038"
PASS = "VJQBOrw29f"

@app.route('/')
def home():
    try:
        with open('index.html', 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return "<h1>خطأ: ملف index.html غير موجود</h1>", 404

# نظام الوسيط الذكي المطور لتخطي حظر السيرفرات الذكية
@app.route('/stream/<stream_id>.m3u8')
def proxy_stream(stream_id):
    target_url = f"{HOST}/live/{USER}/{PASS}/{stream_id}.m3u8"
    
    # بصمة جهاز حقيقي (User-Agent) لإجبار سيرفر IPTV على إرسال البث دون حظر خوادم Render
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": f"{HOST}/",
        "Origin": HOST
    }
    
    try:
        req = requests.get(target_url, stream=True, headers=headers, timeout=10)
        response = Response(req.iter_content(chunk_size=4096), content_type=req.headers.get('Content-Type'))
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except Exception as e:
        return f"<h1>خطأ في الاتصال بسيرفر البث: {str(e)}</h1>", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
