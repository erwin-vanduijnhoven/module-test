import streamlit as st
from clarifai.client.auth import create_stub
from clarifai.client.auth.helper import ClarifaiAuthHelper
from clarifai.client.user import User
from clarifai.modules.css import ClarifaiStreamlitCSS
from google.protobuf import json_format, timestamp_pb2
from PIL import Image
import requests
import io

st.set_page_config(layout="wide")
ClarifaiStreamlitCSS.insert_default_css(st)

# This must be within the display() function.
auth = ClarifaiAuthHelper.from_streamlit(st)
stub = create_stub(auth)
userDataObject = auth.get_user_app_id_proto()
auth_headers = dict(auth.metadata)

# Stream inputs from the app. list_inputs give list of dictionaries with inputs and its metadata .
input_obj = User(user_id=userDataObject.user_id).app(app_id=userDataObject.app_id).inputs()
all_inputs = input_obj.list_inputs(input_type="image", per_page=1)

for input in all_inputs:
  st.title("Show image masks")
  
  response = requests.get(input.data.image.url, headers=auth_headers)
  image = Image.open(io.BytesIO(response.content))
  st.image(image, caption=input.data.image.url)

  base_image_url = input.data.image.url.rsplit('/', 1)[0]
  annotations = input_obj.list_annotations(batch_input=[input])
  for annotation in annotations:
    for region in annotation.data.regions:
      image_id = region.region_info.mask.image.url.rsplit('/', 1)[1]
      url = f"{base_image_url}/{image_id}"
      response = requests.get(url, headers=auth_headers)
      image = Image.open(io.BytesIO(response.content))
      st.image(image, caption=url)

