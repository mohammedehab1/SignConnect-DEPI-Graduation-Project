import mediapipe as mp
import cv2

class MediaPipeProcessor:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def process_frame(self, frame):
        results = self.hands.process(frame)
        if results.multi_hand_landmarks:
            return results.multi_hand_landmarks[0]
        return None

    def get_fixed_bbox(self, hand_landmarks, w, h, size=224):
        xs = [lm.x * w for lm in hand_landmarks.landmark]
        ys = [lm.y * h for lm in hand_landmarks.landmark]
        x_center = int(sum(xs)/len(xs))
        y_center = int(sum(ys)/len(ys))
        x1 = max(0, x_center - size//2)
        y1 = max(0, y_center - size//2)
        x2 = min(w, x_center + size//2)
        y2 = min(h, y_center + size//2)
        return x1, y1, x2, y2
    
    def is_hand_in_allowed_area(self,hand_landmarks, w, h):
        x_min_area = 0 // 2
        x_max_area = w // 2
        y_min_area = h // 4
        y_max_area = 3 * h // 4

        xs = [lm.x * w for lm in hand_landmarks.landmark]
        ys = [lm.y * h for lm in hand_landmarks.landmark]

        hand_x = int(sum(xs) / len(xs))
        hand_y = int(sum(ys) / len(ys))

        return (x_min_area < hand_x < x_max_area) and (y_min_area < hand_y < y_max_area)
    
    def apply_glow(self, frame, x1, y1, x2, y2):
        overlay = frame.copy()
        glow_color = (0, 255, 0)
        alpha = 0.35
        cv2.rectangle(overlay, (x1, y1), (x2, y2), glow_color, -1)
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)