import cv2

cap = cv2.VideoCapture(0)  

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()
    
user = "didi"

# Define filenames for keys 1 to 6
file_names = {
    ord('1'): "dataset/" + user + "/face/front1.jpg",
    ord('2'): "dataset/" + user + "/face/front2.jpg",
    ord('3'): "dataset/" + user + "/face/occ1.jpg",
    ord('4'): "dataset/" + user + "/face/occ2.jpg",
    ord('5'): "dataset/" + user + "/face/pose1.jpg",
    ord('6'): "dataset/" + user + "/face/pose2.jpg"
}

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Could not capture a frame.")
        exit()

    cv2.imshow("frame", frame)

    key = cv2.waitKey(1) & 0xFF

    # Check if key pressed is in the file_names dictionary
    if key in file_names:
        cv2.imwrite(file_names[key], frame)
        print(f"Image captured and saved as '{file_names[key]}'")

    elif key == 27:  # Esc key
        break

cap.release()
cv2.destroyAllWindows()
