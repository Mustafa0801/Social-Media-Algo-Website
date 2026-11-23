import streamlit as st
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates


st.title("Capacitative Touchscreens")
st.write(" ")
st.write("Hello world!")

touchpad = Image.new("RGB", (200, 350), color = (0, 0, 0))


value = streamlit_image_coordinates(touchpad, key="image1")
if value is not None:
    st.write(f"Coordinates: {value['x']}, {value['y']}")