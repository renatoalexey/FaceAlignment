from flask import Flask, jsonify, request
import os
import json
import ast
import utils

correspondet_points = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 10, 10: 18, 11: 20, 12: 23, 13: 37, 15: 38, 17: 40, 18: 48, 19: 28, 20: 29, 21: 30, 22: 31, 25: 32, 28: 53, 26: 49, 29: 13} 
vertical_point_a = 11
vertical_point_b = 8
horizontal_point_a = 0
horizontal_point_b = 18

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

    #print(f"Fiducials folder: {fiducials_folder}")
    
    if os.path.exists(fiducials_folder):
        with open(fiducials_folder, 'r') as file:
            lines = file.readlines()
            for line in lines:
                x, y = line.split(',')
                x = float(x)
                y = float(y)
                ground_truth_pts.append((x, y))

    return jsonify({"ground_truth_pt": ground_truth_pts})

@app.route("/teste", methods=["GET"])
def get_teste():
    fiducials_folder = str(request.args.get("fiducials_folder"))
    library_pts = request.args.get("library_pts")
    print(f"Fiducial points: {fiducials_folder}")
    pontos = ast.literal_eval(library_pts.strip("'"))
    print(f"Library points: {pontos}")
    #library_pts = json.loads(request.args.get("library_pts"))

    gt_pts = folders_teste(fiducials_folder)
    utils.compare_points()

    return jsonify({"teste": 123})

def folders_teste(fiducials_file_path):

    ground_truth_pts = []

    #print(f"Fiducials folder: {fiducials_folder}")
    
    if os.path.exists(fiducials_file_path):
        with open(fiducials_file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                x, y = line.split(',')
                x = float(x)
                y = float(y)
                ground_truth_pts.append((x, y))

    return ground_truth_pts

if __name__ == "__main__":
    # 0.0.0.0 = acessível de outros dispositivos da rede
    app.run(host="0.0.0.0", port=5000, debug=True)
