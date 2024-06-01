import streamlit as st
from keras.models import load_model
from PIL import Image
import numpy as np
import leafmap.foliumap as leafmap


from util import classify, set_background


st.set_page_config(layout="wide")

# Customize the sidebar
markdown = """
Web App URL: <https://castingsample.streamlit.app/>
GitHub Repository: <https://github.com/TaufiiquRahman/Casting_Sample>
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

# Customize page title
st.title("Quality Control Casting Production")

st.markdown(
    """
    This multipage app template demonstrates various interactive web apps created using [streamlit](https://streamlit.io) and [leafmap](https://leafmap.org). It is an open-source project and you are very welcome to contribute to the [GitHub repository](https://github.com/giswqs/streamlit-multipage-template).
    """
)






#set_background('./bgrd/bg.jpg')


# set header
st.header('Please upload a Casting Product Image')

# upload file
file = st.file_uploader('', type=['jpeg', 'jpg', 'png'])



# load classifier
model = load_model('./modelcast.h5')

# load class names
with open('./model/label.txt', 'r') as f:
    class_names = [a[:-1].split(' ')[1] for a in f.readlines()]
    f.close()


# display image
if file is not None:
    image = Image.open(file).convert('RGB')
    st.image(image, use_column_width=True)

    # classify image
    class_name, conf_score = classify(image, model, class_names)

    # write classification
    st.write("## {}".format(class_name))
    st.write("### score: {}%".format(int(conf_score * 1000) / 10))

    m = leafmap.Map(minimap_control=True)
    m.add_basemap("OpenTopoMap")
    m.to_streamlit(height=500)
