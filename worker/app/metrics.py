from prometheus_client import Histogram

shop_order_processing_duration_seconds = Histogram(
    "shop_order_processing_duration_seconds",
    "Time spent by worker processing one order",
    buckets=(0.1, 0.5, 1, 2, 2.1, 2.2, 2.5, 3, 5, 10, 30),
)
