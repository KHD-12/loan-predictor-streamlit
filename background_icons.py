import os
import base64
import random
import streamlit as st

def add_local_background_icons():
    image_folder = "assets"
    if not os.path.exists(image_folder):
        st.warning("Assets folder not found.")
        return

    image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if not image_files:
        st.warning("No images in assets folder.")
        return

    icon_html = "<div style='position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1;'>"
    
    for _ in range(8):  # Display 8 random icons
        image_file = random.choice(image_files)
        with open(os.path.join(image_folder, image_file), "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        
        top = random.randint(5, 90)
        left = random.randint(5, 90)
        size = random.randint(40, 80)
        
        icon_html += f"""
        <img src="data:image/png;base64,{encoded}"
             style="position: absolute; top: {top}%; left: {left}%; width: {size}px; height: {size}px; opacity: 0.1;"/>
        """
    
    icon_html += "</div>"
    st.markdown(icon_html, unsafe_allow_html=True)
    print(image_files)

