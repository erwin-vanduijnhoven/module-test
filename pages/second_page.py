import streamlit as st
import streamlit.components.v1 as components
from clarifai.client.auth import create_stub
from clarifai.client.auth.helper import ClarifaiAuthHelper
from clarifai.client.user import User
from clarifai.modules.css import ClarifaiStreamlitCSS
from google.protobuf import json_format, timestamp_pb2
from PIL import Image
import requests
import numpy as np
import io

st.set_page_config(layout="wide")
ClarifaiStreamlitCSS.insert_default_css(st)

# This must be within the display() function.
auth = ClarifaiAuthHelper.from_streamlit(st)
stub = create_stub(auth)
userDataObject = auth.get_user_app_id_proto()
auth_headers = dict(auth.metadata)

# Stream inputs from the app. list_inputs give list of dictionaries with inputs and its metadata .
input_obj = User(user_id=userDataObject.user_id).app(app_id=userDataObject.app_id).list_models(per_page=2)

st.write(input_obj)

