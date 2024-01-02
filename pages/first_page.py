import streamlit as st
from clarifai.client.auth import create_stub
from clarifai.client.auth.helper import ClarifaiAuthHelper
from clarifai.client.user import User
from clarifai.modules.css import ClarifaiStreamlitCSS
from google.protobuf import json_format, timestamp_pb2

st.set_page_config(layout="wide")
ClarifaiStreamlitCSS.insert_default_css(st)

# This must be within the display() function.
auth = ClarifaiAuthHelper.from_streamlit(st)
stub = create_stub(auth)
userDataObject = auth.get_user_app_id_proto()

# Stream inputs from the app. list_inputs give list of dictionaries with inputs and its metadata .
input_obj = User(user_id=userDataObject.user_id).app(app_id=userDataObject.app_id).inputs()
all_inputs = input_obj.list_inputs(per_page=2)

for inp in range(len(all_inputs)):
  input = all_inputs[inp]
  st.image(input.data.image.url, caption='Image')
  for region in input.data.regions:
    st.image(region.data.image.url, caption='region')

