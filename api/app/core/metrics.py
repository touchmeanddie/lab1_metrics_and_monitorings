from prometheus_client import Counter, Histogram

http_requests_total = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "route", "status"],
)

http_request_duration_seconds = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "route"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.075,
             0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0),
)

shop_orders_created_total = Counter(
    "shop_orders_created_total",
    "Total orders created (POST /orders)",
)
