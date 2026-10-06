Примеры вопросов для PromQL:

• Сколько запросов в секунду получает API? 
sum by (route) (rate(http_requests_total[1m]))

• Какой p95 времени ответа POST /orders?
histogram_quantile(
  0.95,
  sum by (le) (rate(http_request_duration_seconds_bucket{route="/orders", method="POST"}[5m]))
)

• Сколько памяти использует контейнер API? 
(по всем контейнерам) 
sum(container_memory_working_set_bytes) / 1024 / 1024

Только API  
(venv) PS D:\1 семестр МАГА\Наблюдаемость распределённых систем\fast_api_project> docker inspect -f '{{.Id}}' $(docker compose ps -q api)
6242edd8eea01e89a4e9cce54a3957f18c363c29baf4df8d42ed970d1efe52d6

container_memory_working_set_bytes{id="/docker/6242edd8eea01e89a4e9cce54a3957f18c363c29baf4df8d42ed970d1efe52d6"} / 1024 / 1024

• Сколько сообщений сейчас ждут обработки в RabbitMQ? rabbitmq_queue_messages_ready{instance="rabbitmq:15692"}

• Сколько заказов сейчас находятся в PROCESSING? shop_stats_orders_processing

• Сколько секунд прошло с момента последнего обработанного заказа? shop_stats_seconds_since_last_processed

• Сколько соединений открыто к PostgreSQL? pg_stat_database_numbackends{datname="lab1obser"}