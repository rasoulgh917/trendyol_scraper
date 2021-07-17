from sqlalchemy import create_engine
from urllib.parse import quote as urlquote
from .config import *
quoted_pass = urlquote(DB_PASSWORD)
engine = create_engine(f"mysql+pymysql://{DB_USER}:{quoted_pass}@{DB_IP}:{DB_PORT}/{DB_NAME}?charset=cp1252")