from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from CloudSentiment.cloud_trainer import Sentimenter
from datetime import datetime
import pytz
import joblib
import os

dirname = os.path.dirname(__file__)
PATH_TO_MODEL = os.path.join(dirname, "..", "model.joblib")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def index():
    return {"greeting": "Hello world"}

@app.get("/predict")
def predict(date_list,
            text_list,
            out_name = "test.csv"):

    sentiment = Sentimenter(date_list, text_list, out_name = out_name)
    sentiment.set_model()
    sentiment.run()
    out_df = sentiment.save_output("api")
    output = out_df.to_json()

    return output

#  "pickup_datetime": pickup_datetime,
#  "pickup_longitude": pickup_longitude,
#  "pickup_latitude": pickup_latitude,
#  "dropoff_longitude": dropoff_longitude,
#  "dropoff_latitude": dropoff_latitude,
#  "passenger_count": passenger_count
#}