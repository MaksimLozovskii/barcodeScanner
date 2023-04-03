from flask import Flask, render_template, request, g
import cv2
from pyzbar.pyzbar import decode
import base64

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def scan_barcode():
  data = ''
  barcode_type = ''

  if request.method == 'POST':
    cap = cv2.VideoCapture(0)
    frame = cap.read()

    # Read fram, detect barcode
    barcodes = decode(frame)

    if barcodes:
      # Decode if exists
      data = barcodes[0].data.decode('utf-8')
      barcode_type = barcodes[0].type
    else:
      data = ''
      barcode_type = ''

    # Export as jpeg
    jpeg = cv2.imencode('.jpg', frame)

    # Convert to base64
    jpeg_b64 = base64.b64encode(jpeg).decode('utf-8')

    cap.release()

    # Pass the base64-encoded frame to the template
    return render_template('scan_barcode.html', barcode=data, barcode_type=barcode_type, frame=jpeg_b64)
  return render_template('scan_barcode.html', barcode=data, barcode_type=barcode_type)

