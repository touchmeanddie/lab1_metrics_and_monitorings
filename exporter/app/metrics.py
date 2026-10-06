from prometheus_client import Gauge

orders_new = Gauge(
    "shop_stats_orders_new",
    "Orders in status: NEW")

orders_processing = Gauge(
    "shop_stats_orders_processing",
    "Orders in status: PROCESSING")

orders_done = Gauge(
    "shop_stats_orders_done",
    "Orders in status: DONE")

last_processed_at = Gauge(
    "shop_stats_seconds_since_last_processed",
    "Seconds since the last order moved to DONE",
)
