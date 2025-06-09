import cv2
import mediapipe as mp
import pygame

pygame.mixer.init()
thumb_sound = "chord001.wav.mp3"
rock_sound = "chord002.wav.mp3"
peace_sound = "chord003.wav.mp3"
fist_sound = "chord004.wav.mp3"
open_palm_sound = "chord005.wav.mp3"
three_sound = "chord006.wav.mp3"
ok_sign_sound = "chord007.wav.mp3"
point_sound = "chord008.wav.mp3"
call_me_sound = "chord009.wav.mp3"


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
def is_peace_sign(landmarks):
    return (landmarks[8].y < landmarks[6].y and
            landmarks[12].y < landmarks[10].y and
            landmarks[16].y > landmarks[14].y and
            landmarks[20].y > landmarks[18].y)

def is_fist(landmarks):
    return (landmarks[8].y > landmarks[6].y and
            landmarks[12].y > landmarks[10].y and
            landmarks[16].y > landmarks[14].y and
            landmarks[20].y > landmarks[18].y)

def is_open_palm(landmarks):
    return (landmarks[8].y < landmarks[6].y and
            landmarks[12].y < landmarks[10].y and
            landmarks[16].y < landmarks[14].y and
            landmarks[20].y < landmarks[18].y)

def is_three_fingers_up(landmarks):
    return (landmarks[8].y < landmarks[6].y and
            landmarks[12].y < landmarks[10].y and
            landmarks[16].y < landmarks[14].y and
            landmarks[20].y > landmarks[18].y)


def is_ok_sign(landmarks):
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    distance = ((thumb_tip.x - index_tip.x) ** 2 + (thumb_tip.y - index_tip.y) ** 2) ** 0.5
    return distance < 0.05

def is_point_right(landmarks):
    return (landmarks[8].y < landmarks[6].y and
            landmarks[12].y > landmarks[10].y and
            landmarks[16].y > landmarks[14].y and
            landmarks[20].y > landmarks[18].y)

def is_call_me(landmarks):
    return (landmarks[4].y < landmarks[3].y and
            landmarks[20].y < landmarks[18].y and
            landmarks[8].y > landmarks[6].y and
            landmarks[12].y > landmarks[10].y and
            landmarks[16].y > landmarks[14].y)


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
            elif is_peace_sign(landmarks):
                current_gesture = "peace"
            elif is_fist(landmarks):
                current_gesture = "fist"
            elif is_open_palm(landmarks):
                current_gesture = "open_palm"
            elif is_three_fingers_up(landmarks):
                current_gesture = "three"
            elif is_ok_sign(landmarks):
                current_gesture = "ok_sign"
            elif is_point_right(landmarks):
                current_gesture = "point"
            elif is_call_me(landmarks):
                current_gesture = "call_me"


            
            if current_gesture and current_gesture != last_gesture:
                if current_gesture == "thumbs_up":
                    pygame.mixer.music.load(thumb_sound)
                    pygame.mixer.music.play()
                    print("Thumbs up - chord003")
                elif current_gesture == "rock_on":
                    pygame.mixer.music.load(rock_sound)
                    pygame.mixer.music.play()
                    print("Rock on - chord002")
                elif current_gesture == "peace":
                    pygame.mixer.music.load(peace_sound)
                    pygame.mixer.music.play()
                    print("Peace Sign - chord003")
                elif current_gesture == "fist":
                    pygame.mixer.music.load(fist_sound)
                    pygame.mixer.music.play()
                    print("Fist - chord004")
                elif current_gesture == "open_palm":
                    pygame.mixer.music.load(open_palm_sound)
                    pygame.mixer.music.play()
                    print("Open Palm - chord005")
                elif current_gesture == "three":
                    pygame.mixer.music.load(three_sound)
                    pygame.mixer.music.play()
                    print("Victory Pose - chord006")
                elif current_gesture == "ok_sign":
                    pygame.mixer.music.load(ok_sign_sound)
                    pygame.mixer.music.play()
                    print("OK Sign - chord007")
                elif current_gesture == "point":
                    pygame.mixer.music.load(point_sound)
                    pygame.mixer.music.play()
                    print("Point Right - chord008")
                elif current_gesture == "call_me":
                    pygame.mixer.music.load(call_me_sound)
                    pygame.mixer.music.play()
                    print("Call Me - chord009")

                last_gesture = current_gesture
            elif not current_gesture:
                last_gesture = None  

    cv2.imshow("Hand Gesture", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
