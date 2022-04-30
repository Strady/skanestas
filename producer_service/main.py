import time

import schedule

from prices_producer import PricesProducer
from data_publisher import DataPublisher
from config import ServiceConfig


def main() -> None:
    service_config = ServiceConfig()
    publisher = DataPublisher(
        redis_host=service_config.redis_host,
        channel_name=service_config.channel_name,
        producer=PricesProducer(service_config.tickers_number)
    )
    schedule.every().second.do(publisher.publish_prices_data)
    while True:
        schedule.run_pending()
        time.sleep(0.1)


if __name__ == '__main__':
    main()
