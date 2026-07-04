from PIL import Image
import os

# Define input and output paths
input_image_path = "image_3.png"
sidebar_logo_path = "sidebar_logo.png"
main_page_logo_path = "main_page_logo.png"

# Open the original image
if os.path.exists(input_image_path):
    with Image.open(input_image_path) as img:
        # Resize for Sidebar (width 200px, maintaining aspect ratio)
        sidebar_img = img.copy()
        sidebar_width = 200
        w_percent = (sidebar_width / float(sidebar_img.size[0]))
        h_size = int((float(sidebar_img.size[1]) * float(w_percent)))
        sidebar_img = sidebar_img.resize((sidebar_width, h_size), Image.Resampling.LANCZOS)
        sidebar_img.save(sidebar_logo_path)
        print(f"Saved sidebar logo as {sidebar_logo_path}")

        # Resize for Main Page (width 300px, maintaining aspect ratio)
        main_page_img = img.copy()
        main_page_width = 300
        w_percent = (main_page_width / float(main_page_img.size[0]))
        h_size = int((float(main_page_img.size[1]) * float(w_percent)))
        main_page_img = main_page_img.resize((main_page_width, h_size), Image.Resampling.LANCZOS)
        main_page_img.save(main_page_logo_path)
        print(f"Saved main page logo as {main_page_logo_path}")
else:
    print(f"Error: {input_image_path} not found.")
