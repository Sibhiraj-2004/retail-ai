import os
from dotenv import load_dotenv

# 🔥 FORCE absolute path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(dotenv_path=ENV_PATH,override=True)


class Settings:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL")


settings = Settings()

print("DEBUG ENV PATH:", ENV_PATH)
print("DEBUG DB URL:", settings.DATABASE_URL)
