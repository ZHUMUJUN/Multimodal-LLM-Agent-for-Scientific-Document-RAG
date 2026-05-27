import uvicorn
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).resolve().parent / ".env")

import config
from core.logging_utils import configure_logging
from core.tracing import initialize_tracing


if __name__ == "__main__":
    configure_logging()
    initialize_tracing()
    uvicorn.run("api.app:app", host=config.API_HOST, port=config.API_PORT, reload=False)
