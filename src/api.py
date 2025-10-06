from flask import Flask, jsonify, request
import os

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"mensagem": "Servidor Python funcionando 🚀"})

@app.route("/soma", methods=["GET"])
def soma():
    a = int(request.args.get("a", 0))
    b = int(request.args.get("b", 0))
    return jsonify({"resultado": a + b})

@app.route("/ground/truth/points", methods=["GET"])
def get_ground_truth_points():
    fiducials_folder = str(request.args.get("fiducials_folder"))
    ground_truth_pts = []
    
    if os.path.exists(fiducials_folder):
        with open(fiducials_folder, 'r') as file:
            lines = file.readlines()
            for line in lines:
                x, y = line.split(',')
                x = float(x)
                y = float(y)
                ground_truth_pts.append((x, y))

    return jsonify({"ground_truth_pt": ground_truth_pts})

if __name__ == "__main__":
    # 0.0.0.0 = acessível de outros dispositivos da rede
    app.run(host="0.0.0.0", port=5000, debug=True)
