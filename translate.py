from logger_ import logger
try:
    from deep_translator import GoogleTranslator
except:
    logger("Failed to connect to google translate APIs, retrying ...")
    from deep_translator import GoogleTranslator
from deep_translator.exceptions import NotValidLength, NotValidPayload
from requests import exceptions
from redis import Redis
from config import REDIS_SERVER_HOST, REDIS_SERVER_PORT, TRANSLATE

if TRANSLATE:
    re = Redis(host=REDIS_SERVER_HOST, port=REDIS_SERVER_PORT, db=0)

def connect_translate(text: str):
    try:
        return GoogleTranslator(source='tr', target='en').translate(text)
    except NotValidPayload:
        return text
    except ConnectionError:
        return GoogleTranslator(source='tr', target='en').translate(text)
    except NotValidLength:
        return text
    except exceptions.ConnectionError:
        return GoogleTranslator(source='tr', target='en').translate(text)
    except:
        return GoogleTranslator(source='tr', target='en').translate(text)

def translator(text: str):
    if not TRANSLATE:
        return text
    try:
        int(text)
        return text
    except ValueError:
        if re.get(text):
            return re.get(text).decode()
        else:
            translated_text = connect_translate(text)
            re.set(text, translated_text)
        return translated_text
