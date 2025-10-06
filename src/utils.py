import math

def compare_points(ground_truth_pts, library_pts, correspondet_points, vertical_distance=1, horizontal_distance=1):
    all_distances = []

    for i, groud_truth_point in enumerate(ground_truth_pts, start=1):
        if correspondet_points.get(i) is not None:
            fa_point = library_pts[0][correspondet_points.get(i)]
            distance = calcEuclideanDistance(groud_truth_point[0], groud_truth_point[1],
                        fa_point[0], fa_point[0], vertical_distance, horizontal_distance)    
            all_distances.append(distance)
    return all_distances

def calcEuclideanDistance(x1, y1, x2, y2, vertical_distance=1, horizontal_distance=1):
    return round(math.sqrt( ( (x2 - x1) / horizontal_distance ) **2 + ( (y2 - y1) / vertical_distance ) **2), 2)