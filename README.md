🧾 Program Description

The Click Counter program is an interactive Python application that allows users to load an image and record click points visually. When the user clicks anywhere on the displayed image, the program places a red dot at the clicked position and updates a visible count of total clicks on the image in blue text.

It provides a simple and intuitive way to track visual points of interest, measure user interactions, or annotate images for analysis. The counter updates dynamically with every click, and users can also undo, reset, or save their progress.

The interface runs using OpenCV, displaying the image in a resizable window that responds to mouse and keyboard events.

⚙️ Key Features

Red Dot Marking: Each left mouse click adds a red dot to the image.

Click Counter: A live count of clicks is shown in blue at the top-left corner.

Undo Function (U): Removes the most recent dot.

Reset Function (R): Clears all dots and resets the counter to zero.

Save Function (S): Saves the annotated image with a timestamp.

Exit Keys: Press Q or Esc to close the program safely.

🧠 Technologies Used

Python 3.x

OpenCV (cv2) for image rendering and mouse interaction.

OS and Datetime modules for path handling and file management.

🧩 Use Cases

Marking and counting points of interest on images (e.g., defects, objects, or cells).

Recording user click patterns for interaction analysis.

Annotating images for computer vision or data labeling tasks.

Educational demonstrations of OpenCV mouse and keyboard event handling.
