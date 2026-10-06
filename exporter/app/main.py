import logging
import threading
import time
import requests

from datetime import datetime, timezone
from prometheus_client import start_http_server

from app.config import settings
from app.logging_config import setup_logging
from app.metrics import (
    orders_new,
    orders_processing,
    orders_done,
    last_processed_at,
)

setup_logging()
logger = logging.getLogger(__name__)


def poll_api() -> None:
    while True:
        try:
            r = requests.get(f"{settings.api_url}/internal/stats", timeout=5)
            r.raise_for_status()
            data = r.json()

            orders_new.set(data["orders_new"])
            orders_processing.set(data["orders_processing"])
            orders_done.set(data["orders_done"])

            last = data.get("last_processed_at")
            if last:
                last_dt = datetime.fromisoformat(last)
                if last_dt.tzinfo is None:
                    last_dt = last_dt.replace(tzinfo=timezone.utc)
                last_processed_at.set(
                    (datetime.now(timezone.utc) - last_dt).total_seconds()
                )
            else:
                last_processed_at.set(0)
        except Exception:
            logger.exception(
                "Failed to scrape %s/internal/stats", settings.api_url
            )
        time.sleep(settings.scrape_interval_seconds)


def main() -> None:
    start_http_server(settings.exporter_port)
    logger.info(
        "Exporter listening on :%d, scraping %s",
        settings.exporter_port,
        settings.api_url,
    )
    t = threading.Thread(target=poll_api, daemon=True)
    t.start()
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
