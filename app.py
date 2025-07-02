from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/mkpasswd', methods=['POST'])
def hash_password():
    try:
        # Get JSON request data
        data = request.get_json()
        password = data.get('password')

        if not password:
            return jsonify({"error": "Missing password in request"}), 400

        # Run mkpasswd command with SHA-512 hashing
        hashed_password = subprocess.check_output(['mkpasswd', '-m', 'sha-512', '-s', password])
        hashed_password = hashed_password.decode('utf-8').strip()  # Decode bytes to string and strip whitespace

        # Respond with the hashed password
        return jsonify({"success": True, "hashed": hashed_password}), 200

    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Error generating hashed password"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)