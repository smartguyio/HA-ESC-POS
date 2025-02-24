import os
from flask import Flask, request, jsonify
from escpos.printer import Network

app = Flask(__name__)

# Read configuration from environment variables (set by the add-on)
PRINTER_IP = os.getenv("printer_ip", "192.168.1.100")
PRINTER_PORT = int(os.getenv("printer_port", "9100"))

@app.route('/print', methods=['POST'])
def print_text():
    data = request.get_json()
    text = data.get('text')
    
    if not text:
        return jsonify({"error": "Missing 'text' parameter in the request"}), 400

    try:
        # Initialize network printer connection
        printer = Network(PRINTER_IP, port=PRINTER_PORT)
        printer.text(text + "\n")
        printer.cut()
        printer.close()
        return jsonify({"status": "Printed successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # The add-on will be reachable on all network interfaces
    app.run(host='0.0.0.0', port=5000)
