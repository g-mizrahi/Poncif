import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
from poncif_utils import *
from time import time

def headers():
    """
    Set the titles and such.
    Hide the technical menu.
    """
    st.set_page_config(page_title="Poncif - Almaviva", page_icon=":pencil2:", layout="wide")
    hide_menu_style = """<style>#MainMenu {visibility: hidden;}</style>"""
    st.markdown(hide_menu_style, unsafe_allow_html=True)
    st.title("Outil de réalisation de poncif")

def app():
    # The form allows to change multiple parameters before re-rendering the app
    with st.form(key="reload"):

        # 3 columns
        #   1. For the configuration buttons
        #   2. for the canvas
        #   3. for the reload button
        col1, col2, col3 = st.columns((2, 8, 1))

        #   1. background_image is the image to analyse, None by default
        #   2. drawing_mode selects the drawing tool or the eraser
        #   3. stroke_width is the thickness of the strokes
        #   4. high_threshold is the high threshold for the Canny detection
        #   5. low_threshold is the low threshold for the Canny detection
        with col1:
            st.header("Configuration")
            st.session_state["background_image"]    = st.file_uploader("Image :", type=["png", "jpg"])
            st.session_state["drawing_mode"]        = st.selectbox("Mode :", ("Dessin", "Gomme"), 0)
            st.session_state["stroke_width"]        = st.slider("Epaisseur :", 1, 20, 3)
            st.session_state["high_threshold"]      = st.slider("Seuil haut :", 0, 500, 300)
            st.session_state["low_threshold"]       = st.slider("Seuil bas :", 0, 500, 100)
            if "previous_thresholds" not in st.session_state:
                st.session_state["previous_thresholds"] = [st.session_state["high_threshold"], st.session_state["low_threshold"]]
        # The second column is for the canvas
        # If a background image exists it needs to be displayed
        #   the display has to respect the aspect ratio
        #   it needs to make good use of the size of the screen
        with col2:
            if st.session_state["background_image"]:
                # Open the image to display
                bg = Image.open(st.session_state["background_image"])
                # Compute a reasonable size for the display
                target_size = get_target_size(bg.size, (1100, 800))
                # resize the image
                bg_resized = bg.resize(target_size, Image.Resampling.LANCZOS)
                # Set the display size
                st.session_state["w"], st.session_state["h"] = bg_resized.size

                # Compute contours only if they don't already exist or if the thresholds have changed
                # TODO : Look into cached functions with st.cache decorator
                if ("contours" not in st.session_state) or ([st.session_state["high_threshold"], st.session_state["low_threshold"]] != st.session_state["previous_thresholds"]):
                    st.session_state["contours"] = contours2json(get_contours_dict(bg_resized, st.session_state["low_threshold"], st.session_state["high_threshold"]))
                    st.session_state["previous_thresholds"] = [st.session_state["high_threshold"], st.session_state["low_threshold"]]

                # Loading the canvas with the image and the contours
                canvas_result = st_canvas(
                    background_image = bg_resized,
                    stroke_width = st.session_state["stroke_width"],
                    stroke_color = "#ffff00" if st.session_state["drawing_mode"] == "Gomme" else "#000000",
                    height = st.session_state["h"],
                    width = st.session_state["w"],
                    initial_drawing = st.session_state["contours"] if "contours" in st.session_state else None,
                    update_streamlit = True
                )
            
            # If no image is loaded, load an empty canvas
            else:
                print("No image loaded. Loading empty canvas.")

                canvas_result = st_canvas(
                    stroke_width = st.session_state["stroke_width"] if "stroke_width" in st.session_state else 3,
                    height = 600,
                    width = 1000,
                    update_streamlit = True
                )

        # The rest of the logic has nothing to display
        # The goal is to add the drawn paths to the list of contours and reduce all the eraser ones
        if st.session_state["drawing_mode"] == "Dessin":
            # If there are already contours then add the drawn ones and update
            if "contours" in st.session_state and canvas_result.json_data:
                st.session_state["contours"] = add_path_no_duplicate(st.session_state["contours"], canvas_result.json_data)
                # print(st.session_state["contours"])
        
        # If the drawing mode is eraser then find the contour close to the eraser and delete them
        if st.session_state["drawing_mode"] == "Gomme":
        # If there are already contours then add the drawn ones and update
            if "contours" in st.session_state and canvas_result.json_data:
                st.session_state["contours"] = remove_path_too_close(st.session_state["contours"], canvas_result.json_data, st.session_state["stroke_width"])
                # print(st.session_state["contours"])            
        with col3:
            st.form_submit_button('Appliquer les changements')

if __name__=="__main__":
    headers()
    app()