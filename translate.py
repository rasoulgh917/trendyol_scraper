from logger import logger
try:
    from deep_translator import GoogleTranslator
except:
    logger("Failed to connect to google translate APIs, retrying ...")
    from deep_translator import GoogleTranslator
from deep_translator.exceptions import NotValidLength, NotValidPayload
from requests import exceptions
from redis import Redis
from config import REDIS_SERVER_HOST, REDIS_SERVER_PORT, TRANSLATE

def connect_translate(text: str, dest: str):
    try:
        return GoogleTranslator(source='tr', target=dest).translate(text)
    except NotValidPayload:
        return text
    except:
        return GoogleTranslator(source='tr', target=dest).translate(text)

def translator(text: str, dest: str, re):
    try:
        int(text)
        return text
    except ValueError:
        if re.get(text):
            return re.get(text).decode()
        else:
            translated_text = connect_translate(text, dest)
            re.set(text, translated_text)
        return translated_text
