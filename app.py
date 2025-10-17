import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
import google.generativeai as genai

# إعداد مفتاح Gemini من GitHub Secrets
API_KEY = os.environ.get("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.jpeg', '.png', '.pdf']

def allowed_file(filename):
    ext = os.path.splitext(filename)[1].lower()
    return ext in app.config['UPLOAD_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    text = request.form.get('text', '').strip()
    file = request.files.get('file')

    if not text and not file:
        return jsonify({'error': 'يرجى رفع ملف أو إدخال نص التحليل.'}), 400

    file_bytes = None
    if file and file.filename:
        filename = secure_filename(file.filename)
        if not allowed_file(filename):
            return jsonify({'error': 'نوع الملف غير مسموح.'}), 400
        file_bytes = file.read()

    role_prompt = (
        "أنت طبيب افتراضي خبير. اقرأ البيانات المرسلة (صورة أو نص) "
        "وقدم تقريرًا طبيًا مبسطًا، اذكر القيم المهمة، هل هي طبيعية أم لا، "
        "واقترح الخطوات التالية (زيارة طبيب، فحوص إضافية...)."
    )

    try:
        if not API_KEY:
            return jsonify({'warning': 'GEMINI_API_KEY غير مُعد على الخادم.', 
                            'analysis': 'وضع تجريبي: ضع المفتاح للحصول على تحليل حقيقي.'})

        if file_bytes:
            resp = genai.generate(
                model="gemini-1.5-mini",
                input=[
                    {"role": "system", "content": role_prompt},
                    {"role": "user", "content": "حلل الصورة المرفقة وأعط تقرير طبي."},
                ],
                attachments=[{"name": filename, "data": file_bytes}]
            )
            text_out = resp.get('candidates', [{}])[0].get('content', '') if isinstance(resp, dict) else str(resp)
        else:
            prompt = f"{role_prompt}\n\nPatient Report:\n{text}\n\nPlease respond in Arabic."
            resp = genai.generate(
                model="gemini-1.5-mini",
                input=prompt,
                max_output_tokens=800
            )
            text_out = resp.get('candidates', [{}])[0].get('content', '') if isinstance(resp, dict) else str(resp)

        return jsonify({'analysis': text_out})

    except Exception as e:
        return jsonify({'error': 'فشل أثناء المعالجة', 'detail': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
