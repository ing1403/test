import io
import base64
import qrcode
from flask import Flask, render_template, request, send_file

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    qr_image_data = None
    data_to_encode = ""

    if request.method == 'POST':
        data_to_encode = request.form.get('data_to_encode')
        if data_to_encode:
            # สร้าง QR Code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(data_to_encode)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")

            # แปลงภาพเป็น Base64 สำหรับแสดงผลบน HTML
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            qr_image_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
    return render_template('index.html', qr_image_data=qr_image_data)

@app.route('/download_qr', methods=['POST'])
def download_qr():
    data_to_encode_download = request.form.get('data_to_encode_download')

    if data_to_encode_download:
        # สร้าง QR Code อีกครั้งสำหรับการดาวน์โหลด
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H, # ใช้ High error correction สำหรับไฟล์ดาวน์โหลด
            box_size=10,
            border=4,
        )
        qr.add_data(data_to_encode_download)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # เตรียมไฟล์สำหรับการดาวน์โหลด
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0) # ย้ายตำแหน่ง pointer ไปที่จุดเริ่มต้นของ buffer

        return send_file(
            buffer,
            mimetype='image/png',
            as_attachment=True,
            download_name=f'qrcode_{data_to_encode_download[:20]}.png' # ตั้งชื่อไฟล์ให้ไม่ซ้ำกัน
        )
    return "No data provided for download.", 400 # ถ้าไม่มีข้อมูลจะส่งรหัส 400

if __name__ == '__main__':
    app.run(debug=True) # debug=True จะช่วยในการพัฒนา (รีโหลดอัตโนมัติเมื่อมีการเปลี่ยนแปลง)