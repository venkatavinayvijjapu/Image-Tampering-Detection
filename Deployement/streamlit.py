import streamlit as st
import pickle
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
import time
import requests
# PRE-PROCESSING THE IMAGE FOR TESTING
from PIL import Image, ImageChops, ImageEnhance
import os
import itertools

# st.snow()
st.set_page_config(page_title='C-13 Mini project', page_icon='😁')
st.markdown(""" <style>

MainMenu {visibility: hidden;}
header {visibility:hidden;}
footer {visibility: hidden;}
[data-testid="stAppViewContainer"]{
# background-image: url("https://tse4.mm.bing.net/th?id=OIP.j152CjiQZAA7hdfvkhqZBQHaE6&pid=Api&P=0");
background-color:cover;
}
</style> """, unsafe_allow_html=True)


# page_bg_img="""
# <style>
# [data-testid="stAppViewContainer"]{
# background-image: url("C:\Users\vijja\PycharmProjects\pythonProject43\th (4).jpeg");
# background-color:cover;
# }
# </style>
# """
# st.markdown(page_bg_img,unsafe_allow_html=True)
model = load_model("model1.h5")
def convert_to_ela_image(path, quality):
    temp_filename = 'temp_file.jpg'
    ela_filename = 'temp_ela_file.png'

    image = Image.open(path).convert('RGB')
    image.save(temp_filename, 'JPEG', quality=quality)
    temp_image = Image.open(temp_filename)

    ela_image = ImageChops.difference(image, temp_image)

    extrema = ela_image.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    if max_diff == 0:
        max_diff = 1
    scale = 255.0 / max_diff

    ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)

    return ela_image

image_size = (128,128)

def prepare_image(image_path):
    return np.array(convert_to_ela_image(image_path, 85).resize(image_size)).flatten() / 255.0

def predict(imge):
    ela_img=prepare_image(imge)
    ela_img = ela_img.reshape(-1, 128, 128, 3)
    arr = model.predict(ela_img)
    print(arr)
    if (arr[0][0] > arr[0][1]):
        return "IMAGE IS TAMPERED"
    else:
        return "IMAGE IS AUTHENTICATED";

# img_url = st.text_input(label='Enter Image URL')

# if (img_url != "") or (img_url != None):
#     img = Image.open(requests.get(img_url, stream=True).raw)
#     img.save('vvv.jpg')
#     st.image(img)

imge=st.file_uploader('Upload your file', type=['JPG', 'PNG', 'JPEG', 'TIF'], accept_multiple_files=False, key=None, help=None,
                 on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible")

if(imge!=None):
    st.image(imge, caption='Uploaded Image')
# if(imge==None and img_url!=None):
#     imeg=img
if st.button('Predict'):
    with st.spinner(text="Checking....."):
        time.sleep(5)
        predict=predict(imge)
        # if(img_url!=None):
        #     predict = predict('vvv.jpg')
    st.write(predict)
#     recommend=recommendation(option)
#     for i in recommend:

#         st.write(i)