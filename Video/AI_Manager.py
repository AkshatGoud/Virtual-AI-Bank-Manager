import cv2

video_path = r"C:\Users\aryan\OneDrive\Desktop\StandardChartered\Manager.mp4"

def play_video(video_path):
    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('AI Branch Manager', frame)
        
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Play the AI Manager's video
play_video("Manager.mp4")  # Use the video from Synthesia/D-ID
