from os import getenv

from dotenv import load_dotenv

load_dotenv()

# Auth config
SECRET_KEY = str(getenv("SECRET_KEY"))
ALGORITHM = str(getenv("ALGORITHM"))
ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Database config
LOGIN_USER = str(getenv("LOGIN_USER"))
PASSWORD = str(getenv("PASSWORD"))
SERVERNAME = str(getenv("SERVERNAME"))
DBNAME = str(getenv("DBNAME"))
DRIVER = str(getenv("DRIVER"))
