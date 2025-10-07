# ------------------------------------------------------------
# click_counter.py
# Click on the image to add red dots and keep a live count
# Keys: Q/Esc=quit, R=reset, U=undo last dot, S=save annotated
# ------------------------------------------------------------
import cv2
import os
import glob
from datetime import datetime

# -----------------------------
# USER DEFAULTS
# -----------------------------
# 1) We expect the file to be here based on your note:
DEFAULT_EXPECTED = r"C:\Users\maste\Desktop\image.png"
# 2) If not found, we will search this folder for an image:
FALLBACK_DIR = r"C:\Users\maste\Desktop"

# Dot & HUD settings
DOT_RADIUS = 5
DOT_COLOR = (0, 0, 255)   # Red (BGR)
DOT_THICKNESS = -1        # Filled
FONT = cv2.FONT_HERSHEY_SIMPLEX
HUD_POS = (10, 30)
HUD_SCALE = 1
HUD_COLOR = (255, 0, 0)   # 🔵 Blue for Count
HUD_THICK = 2

WINDOW_NAME = "Click Counter (Q/Esc quit • R reset • U undo • S save)"

# -----------------------------
# Image resolution & path logic
# -----------------------------
def find_image():
    # If the exact expected path exists, use it.
    if os.path.isfile(DEFAULT_EXPECTED):
        return DEFAULT_EXPECTED

    # Else, if FALLBACK_DIR is a directory, scan it for common image files
    if os.path.isdir(FALLBACK_DIR):
        exts = ("*.png", "*.jpg", "*.jpeg", "*.bmp", "*.tif", "*.tiff")
        candidates = []
        for ext in exts:
            candidates.extend(glob.glob(os.path.join(FALLBACK_DIR, ext)))
        if candidates:
            # Use the first found image (or choose newest)
            return candidates[0]

    # Nothing found
    return None

image_path = find_image()
if not image_path:
    raise FileNotFoundError(
        "No image found.\n"
        f"Tried:\n - {DEFAULT_EXPECTED}\n - Searching in: {FALLBACK_DIR} for common image types.\n"
        "Please place your image on Desktop as 'image.png' or set DEFAULT_EXPECTED/FALLBACK_DIR."
    )

img = cv2.imread(image_path)
if img is None:
    raise ValueError(f"Failed to load image at: {image_path}\n"
                     "Check that the path points to a real image file (e.g., .png, .jpg).")

# Working canvas and state
canvas = img.copy()
points = []  # store clicked (x, y)

def redraw():
    """Redraw the image: original + all dots + HUD."""
    global canvas
    canvas = img.copy()
    # Draw existing points
    for (x, y) in points:
        cv2.circle(canvas, (x, y), DOT_RADIUS, DOT_COLOR, DOT_THICKNESS, lineType=cv2.LINE_AA)
    # Draw HUD last — in BLUE
    cv2.putText(canvas, f"Count: {len(points)}", HUD_POS, FONT, HUD_SCALE, HUD_COLOR, HUD_THICK, cv2.LINE_AA)
    cv2.imshow(WINDOW_NAME, canvas)

def on_mouse(event, x, y, flags, userdata):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        redraw()

# Setup window & callback
cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_AUTOSIZE)
cv2.setMouseCallback(WINDOW_NAME, on_mouse)
redraw()

# -----------------------------
# Event loop
# -----------------------------
while True:
    key = cv2.waitKey(20) & 0xFF
    if key in (27, ord('q')):  # Esc or Q
        break
    elif key == ord('r'):      # Reset
        points.clear()
        redraw()
    elif key == ord('u'):      # Undo last dot
        if points:
            points.pop()
            redraw()
    elif key == ord('s'):      # Save annotated
        base, ext = os.path.splitext(image_path)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_path = f"{base}_annotated_{timestamp}.png"
        # Ensure current canvas reflects all dots and HUD
        redraw()
        cv2.imwrite(out_path, canvas)
        # Brief visual toast
        temp = canvas.copy()
        cv2.putText(temp, f"Saved: {os.path.basename(out_path)}",
                    (10, 60), FONT, 0.7, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow(WINDOW_NAME, temp)
        cv2.waitKey(500)
        cv2.imshow(WINDOW_NAME, canvas)

cv2.destroyAllWindows()

