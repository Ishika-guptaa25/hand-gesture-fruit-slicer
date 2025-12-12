import cv2
import mediapipe as mp
import numpy as np
import time


class HandDetector:
    def __init__(self, mode=False, max_hands=1, detection_con=0.7, track_con=0.7, smooth=True):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_con = detection_con
        self.track_con = track_con
        self.smooth = smooth

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.detection_con,
            min_tracking_confidence=self.track_con
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.tip_ids = [4, 8, 12, 16, 20]

        # smoothing state
        self.prev_x = None
        self.prev_y = None
        self.prev_time = None
        self.speed = 0.0

        self.lm_list = []
        self.results = None

    def find_hands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(
                        img, hand_lms, self.mp_hands.HAND_CONNECTIONS
                    )
        return img

    def find_position(self, img, hand_no=0, draw=True):
        self.lm_list = []
        if self.results and self.results.multi_hand_landmarks:
            if hand_no < len(self.results.multi_hand_landmarks):
                my_hand = self.results.multi_hand_landmarks[hand_no]

                h, w, c = img.shape
                for id, lm in enumerate(my_hand.landmark):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    self.lm_list.append([id, cx, cy])

                    if draw and id == 8:
                        cv2.circle(img, (cx, cy), 8, (255, 0, 255), cv2.FILLED)
        return self.lm_list

    def fingers_up(self):
        fingers = []
        if len(self.lm_list) != 0:
            # Thumb (approx)
            if self.lm_list[self.tip_ids[0]][1] > self.lm_list[self.tip_ids[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            # 4 Fingers
            for id in range(1, 5):
                if self.lm_list[self.tip_ids[id]][2] < self.lm_list[self.tip_ids[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
        return fingers

    def get_index_finger_position(self):
        # returns smoothed coords and speed
        if len(self.lm_list) > 8:
            x, y = self.lm_list[8][1], self.lm_list[8][2]

            now = time.time()
            if self.prev_time is None:
                self.prev_time = now
                self.prev_x, self.prev_y = x, y
                self.speed = 0.0
                return x, y, self.speed

            dt = now - self.prev_time
            if dt <= 0:
                dt = 1 / 60.0

            # raw speed (pixels per second)
            raw_speed = ((x - self.prev_x) ** 2 + (y - self.prev_y) ** 2) ** 0.5 / dt

            # smoothing positions
            if self.smooth and self.prev_x is not None:
                alpha = 0.75  # higher means more smoothing
                sx = int(self.prev_x * alpha + x * (1 - alpha))
                sy = int(self.prev_y * alpha + y * (1 - alpha))
            else:
                sx, sy = x, y

            # update stored values
            self.speed = raw_speed
            self.prev_x, self.prev_y = sx, sy
            self.prev_time = now

            return sx, sy, self.speed

        return None, None, 0.0
