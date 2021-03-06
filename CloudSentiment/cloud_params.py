import os

dirpath = os.getcwd()
LOCAL_PATH = os.path.join(dirpath,"..","raw_data")
LOCAL_CRYPTO_PATH = os.path.join(dirpath,"..","raw_data","crypto_reddit.csv")
LOCAL_ECON_PATH = os.path.join(dirpath,"..","raw_data", "crypto_econ_prelim.csv")
KEY_PATH = os.path.join(dirpath, "keys.json")
BUCKET_NAME = "wagon-data-750-btc-sent-fc"
BUCKET_SENT_FOLDER = "sent_data"
BUCKET_DATA_FOLDER = "raw_data"
BUCKET_MODEL_FOLDER = "model"
GS_DATA_CRYPTO_PATH = f"gcs://{BUCKET_NAME}/{BUCKET_DATA_FOLDER}/crypto_reddit.csv"
GS_DATA_ECON_PATH = f"gcs://{BUCKET_NAME}/{BUCKET_DATA_FOLDER}/crypto_econ_prelim.csv"
GS_SENT_PATH = f"gcs://{BUCKET_NAME}/{BUCKET_SENT_FOLDER}/"
GS_MODEL_PATH = f"gcs://{BUCKET_NAME}/{BUCKET_MODEL_FOLDER}/"
GS_TWEET_PATH = f"gcs://{BUCKET_NAME}/"