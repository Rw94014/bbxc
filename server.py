from flask import Flask, Response, request, abort, jsonify
import os
import json

app = Flask(__name__)

# THE ONLY VALID LICENSE KEY (hardcoded in server)
MASTER_LICENSE_KEY = "FLIGHT-hYcH4FNCehO1yZq2Epq1PHIb3"

# File to store authorized HWIDs
HWID_DB_FILE = 'authorized_hwids.json'

def load_authorized_hwids():
    """Load authorized HWIDs"""
    if os.path.exists(HWID_DB_FILE):
        with open(HWID_DB_FILE, 'r') as f:
            return json.load(f)
    return []

def save_authorized_hwids(hwids):
    """Save authorized HWIDs"""
    with open(HWID_DB_FILE, 'w') as f:
        json.dump(hwids, f, indent=2)

@app.route('/activate', methods=['POST'])
def activate():
    """Validate license key and authorize HWID"""
    data = request.get_json()
    
    license_key = data.get('license_key', '').strip()
    hwid = data.get('hwid', '').strip()
    
    if not license_key or not hwid:
        return jsonify({'error': 'Missing license key or HWID'}), 400
    
    # Validate the master license key
    if license_key != MASTER_LICENSE_KEY:
        print(f"❌ Invalid license key attempted: {license_key}")
        return jsonify({'error': 'Invalid license key'}), 403
    
    # Load authorized HWIDs
    authorized_hwids = load_authorized_hwids()
    
    # Check if already authorized
    if hwid in authorized_hwids:
        print(f"✅ HWID already authorized: {hwid}")
        return jsonify({'success': True, 'message': 'Already activated'}), 200
    
    # Add new HWID
    authorized_hwids.append(hwid)
    save_authorized_hwids(authorized_hwids)
    
    print(f"✅ NEW HWID AUTHORIZED: {hwid}")
    print(f"📊 Total authorized HWIDs: {len(authorized_hwids)}")
    
    return jsonify({'success': True, 'message': 'Activation successful'}), 200

@app.route('/get-main')
def get_main():
    """Validate HWID and serve main.py"""
    hwid = request.headers.get('X-HWID', '').strip()
    
    if not hwid:
        print("❌ No HWID provided")
        abort(403)
    
    # Load authorized HWIDs
    authorized_hwids = load_authorized_hwids()
    
    # Check if HWID is authorized
    if hwid not in authorized_hwids:
        print(f"❌ Unauthorized HWID: {hwid}")
        abort(403)
    
    # Serve main.py
    try:
        with open('main.py', 'r', encoding='utf-8') as f:
            code = f.read()
        
        print(f"✅ Served main.py to authorized HWID: {hwid}")
        return Response(code, mimetype='text/plain; charset=utf-8')
    
    except FileNotFoundError:
        print("❌ main.py not found!")
        abort(500)

@app.route('/revoke', methods=['POST'])
def revoke():
    """Revoke a HWID (admin endpoint)"""
    data = request.get_json()
    hwid_to_revoke = data.get('hwid', '').strip()
    
    if not hwid_to_revoke:
        return jsonify({'error': 'No HWID provided'}), 400
    
    authorized_hwids = load_authorized_hwids()
    
    if hwid_to_revoke in authorized_hwids:
        authorized_hwids.remove(hwid_to_revoke)
        save_authorized_hwids(authorized_hwids)
        print(f"🗑️  REVOKED HWID: {hwid_to_revoke}")
        return jsonify({'success': True, 'message': 'HWID revoked'}), 200
    
    return jsonify({'error': 'HWID not found'}), 404

@app.route('/status')
def status():
    """Check server status and total activations"""
    authorized_hwids = load_authorized_hwids()
    return jsonify({
        'status': 'online',
        'total_activations': len(authorized_hwids)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
