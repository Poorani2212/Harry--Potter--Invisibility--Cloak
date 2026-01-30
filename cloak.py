import cv2
import numpy as np
import time

# 🎥 Camera start
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# ⏳ Camera warm-up
time.sleep(2)

# 📸 Background capture
print("Background capture... Please move away")
background = None
for i in range(30):
    ret, background = cap.read()

# Mirror background
background = cv2.flip(background, 1)

print("Magic started 🪄 Press 'q' to quit")

# 🪄 Main loop
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Mirror frame
    frame = cv2.flip(frame, 1)

    # Convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 🔵 Navy Blue HSV range
    lower_blue = np.array([100, 60, 30])
    upper_blue = np.array([130, 255, 180])

    # Mask creation
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Noise removal
    kernel = np.ones((3,3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel)

    # Invert mask
    mask_inv = cv2.bitwise_not(mask)

    # Background part
    cloak_area = cv2.bitwise_and(background, background, mask=mask)

    # Normal visible part
    normal_area = cv2.bitwise_and(frame, frame, mask=mask_inv)

    # Final output
    final = cv2.add(cloak_area, normal_area)

    cv2.imshow("Harry Potter Invisibility Cloak 🪄", final)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()