import boto3
import cv2

# --- Configura o cliente Rekognition ---
rekognition = boto3.client("rekognition", region_name="us-east-1")
print(rekognition.list_collections())

# --- Lê a imagem local ---
image_path = "01.jpg"
with open(image_path, "rb") as img_file:
    img_bytes = img_file.read()

# --- Chama o Rekognition ---
response = rekognition.detect_faces(
    Image={'Bytes': img_bytes},
    Attributes=['ALL']
)

# --- Carrega imagem no OpenCV ---
img = cv2.imread(image_path)
h, w, _ = img.shape

i = 1
# --- Para cada rosto detectado ---
for face in response["FaceDetails"]:
    for landmark in face["Landmarks"]:
        if i == 12 and i == 15 and i == 19:
            continue
        x = int(landmark["X"] * w)
        y = int(landmark["Y"] * h)
        # Desenha ponto
        cv2.circle(img, (x, y), 3, (0, 0, 255), -1)
        # Opcional: escreve o tipo do landmark
        cv2.putText(img, str(i), (x+5, y-5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
        i += 1

# --- Salva imagem resultante ---
cv2.imwrite("rosto_com_landmarks.jpg", img)
print("Imagem com landmarks salva em rosto_com_landmarks.jpg")
