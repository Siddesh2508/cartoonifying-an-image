import cv2
import easygui
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
from tkinter import Button
from PIL import Image, ImageTk
import os
import sys

# Create GUI window
top = tk.Tk()
top.geometry('500x400')
top.title('Cartoonify Your Image')
top.configure(background='white')


# Function to upload image
def upload():
    image_path = easygui.fileopenbox()

    if image_path:
        cartoonify(image_path)


# Main cartoonify function
def cartoonify(image_path):

    # Read image
    original_image = cv2.imread(image_path)

    if original_image is None:
        print("Cannot open image")
        sys.exit()

    # Convert to RGB
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

    # Resize
    resized1 = cv2.resize(original_image, (600, 400))

    # Convert to grayscale
    gray_image = cv2.cvtColor(original_image, cv2.COLOR_RGB2GRAY)
    resized2 = cv2.resize(gray_image, (600, 400))

    # Apply median blur
    smooth_gray = cv2.medianBlur(gray_image, 5)
    resized3 = cv2.resize(smooth_gray, (600, 400))

    # Detect edges
    edges = cv2.adaptiveThreshold(
        smooth_gray,
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        9,
        9
    )

    resized4 = cv2.resize(edges, (600, 400))

    # Apply bilateral filter
    color_image = cv2.bilateralFilter(original_image, 9, 300, 300)
    resized5 = cv2.resize(color_image, (600, 400))

    # Cartoon effect
    cartoon_image = cv2.bitwise_and(color_image, color_image, mask=edges)
    resized6 = cv2.resize(cartoon_image, (600, 400))

    # Plot images
    images = [
        resized1,
        resized2,
        resized3,
        resized4,
        resized5,
        resized6
    ]

    fig, axes = plt.subplots(
        3,
        2,
        figsize=(8, 8),
        subplot_kw={'xticks': [], 'yticks': []}
    )

    titles = [
        "Original Image",
        "Gray Image",
        "Blurred Image",
        "Edge Mask",
        "Filtered Image",
        "Cartoon Image"
    ]

    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')
        ax.set_title(titles[i])

    plt.tight_layout()

    # Save button
    save_button = Button(
        top,
        text="Save Cartoon Image",
        command=lambda: save(cartoon_image, image_path),
        padx=20,
        pady=5
    )

    save_button.configure(
        background='#364156',
        foreground='white',
        font=('calibri', 10, 'bold')
    )

    save_button.pack(side=tk.BOTTOM, pady=20)

    plt.show()


# Save image
def save(cartoon_image, image_path):

    new_name = "cartoonified_image"

    path1 = os.path.dirname(image_path)

    extension = os.path.splitext(image_path)[1]

    path = os.path.join(path1, new_name + extension)

    cv2.imwrite(path, cv2.cvtColor(cartoon_image, cv2.COLOR_RGB2BGR))

    messagebox.showinfo(
        title="Image Saved",
        message=f"Image saved at:\n{path}"
    )


# Webcam capture
def capture():

    cam = cv2.VideoCapture(0)

    while True:

        ret, frame = cam.read()

        if not ret:
            print("Failed to capture")
            break

        cv2.imshow("Capture Image", frame)

        key = cv2.waitKey(1)

        # ESC key
        if key == 27:
            break

        # SPACE key
        elif key == 32:

            img_name = "captured_image.png"

            cv2.imwrite(img_name, frame)

            print(f"{img_name} saved!")

            cartoonify(img_name)

            break

    cam.release()

    cv2.destroyAllWindows()


# Upload button
upload_button = Button(
    top,
    text="Cartoonify an Image",
    command=upload,
    padx=20,
    pady=5
)

upload_button.configure(
    background='#364156',
    foreground='white',
    font=('calibri', 12, 'bold')
)

upload_button.pack(pady=30)


# Capture button
capture_button = Button(
    top,
    text="Capture From Webcam",
    command=capture,
    padx=20,
    pady=5
)

capture_button.configure(
    background='#364156',
    foreground='white',
    font=('calibri', 12, 'bold')
)

capture_button.pack(pady=20)

top.mainloop()