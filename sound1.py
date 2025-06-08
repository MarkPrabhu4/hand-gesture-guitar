import cv2
import mediapipe as mp
import pygame

pygame.mixer.init()
thumb_sound = "chord001.wav.mp3"
rock_sound = "chord002.wav.mp3"  

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

last_gesture = None  

def is_thumb_up(landmarks):
    return landmarks[4].y < landmarks[3].y < landmarks[2].y and landmarks[4].x < landmarks[5].x

def is_rock_on(landmarks):
    index_up = landmarks[8].y < landmarks[6].y
    pinky_up = landmarks[20].y < landmarks[18].y
    middle_down = landmarks[12].y > landmarks[10].y
    ring_down = landmarks[16].y > landmarks[14].y
    return index_up and pinky_up and middle_down and ring_down

while True:
    success, img = cap.read()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    current_gesture = None

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)
            landmarks = handLms.landmark

            if is_thumb_up(landmarks):
                current_gesture = "thumbs_up"
            elif is_rock_on(landmarks):
                current_gesture = "rock_on"

            
            if current_gesture and current_gesture != last_gesture:
                if current_gesture == "thumbs_up":
                    pygame.mixer.music.load(thumb_sound)
                    pygame.mixer.music.play()
                    print("Thumbs up - chord003")
                elif current_gesture == "rock_on":
                    pygame.mixer.music.load(rock_sound)
                    pygame.mixer.music.play()
                    print("Rock on - chord002")
                last_gesture = current_gesture
            elif not current_gesture:
                last_gesture = None  

    cv2.imshow("Hand Gesture", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
