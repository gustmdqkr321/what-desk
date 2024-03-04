from ultralytics import YOLO
import os
import cv2
import csv
def detect(image_path, result_folder, conf_threshold=0.25):
    from ultralytics import YOLO
    # Load model
    # model = YOLO("yolov8s.pt")
    model = YOLO("yolov8x.pt")
    # Predict
    result = model.predict(image_path, save=False, conf=conf_threshold, classes =[24,25,26,39,41,56,58,59,60,62,63,64,66,73,74,])

    # 이미지 저장 경로
    file_name = os.path.splitext(os.path.basename(image_path))[0]

    # 저장 경로
    save_path = os.path.join(result_folder, f"{file_name}_result.jpg")

    # 저장
    plots = result[0].plot()
    cv2.imwrite(save_path, plots)

    return save_path

if __name__ == "__main__":
    # 결과 이미지를 저장할 폴더 생성
    result_folder = "/Users/park_sh/Desktop/what-desk/back/result"
    os.makedirs(result_folder, exist_ok=True)

    # YOLO 모델 로드
    model = YOLO("yolov8s.pt")

    # 이미지 경로
    image_paths = 'image'

    for file_name in os.listdir(image_paths):
        if file_name.endswith((".jpg", ".jpeg", ".png")):
            image_path = os.path.join(image_paths, file_name)
            result_image_path = detect(image_path, result_folder,0.1)