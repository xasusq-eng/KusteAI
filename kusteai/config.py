import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    api_key: str
    base_url: str
    model: str
    owner_name: str
    db_path: str
    max_search_results: int
    owner_pin: str
    adb_path: str



def get_settings() -> Settings:
    return Settings(
        api_key=os.getenv("KUSTEAI_API_KEY", ""),
        base_url=os.getenv("KUSTEAI_BASE_URL", "https://api.openai.com/v1"),
        model=os.getenv("KUSTEAI_MODEL", "gpt-4o-mini"),
        owner_name=os.getenv("KUSTEAI_OWNER_NAME", "owner"),
        db_path=os.getenv("KUSTEAI_DB_PATH", "kusteai.db"),
        max_search_results=int(os.getenv("KUSTEAI_MAX_SEARCH_RESULTS", "5")),
        owner_pin=os.getenv("KUSTEAI_OWNER_PIN", "0000"),
        adb_path=os.getenv("KUSTEAI_ADB_PATH", "adb"),
    )
