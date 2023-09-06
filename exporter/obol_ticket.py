import logging
import time

from prometheus_client import start_http_server, Gauge

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(filename)s[line:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%dT%H:%M:%SZ',
                    filemode='a')
logger = logging.getLogger()

prefix_url = 'https://prater.beaconcha.in/validator/'
# prefix_url = 'https://prater.beaconcha.in/validatorfdfds/'
validator_index_list = [
    379336,
]


def get_label(prefix_url, ovalidator_index):
    obol_labels = dict()
    import requests
    from bs4 import BeautifulSoup
    url = prefix_url + str(ovalidator_index)
    headers = {
        'Cookie': '_ga=GA1.2.1172375884.1662000942; _gid=GA1.2.1872667178.1662000942; cookie=accepted; _gorilla_csrf=MTY2MjAwMDk2MnxJbEpqV1ZCb1pITmpUMDF6ZFdkUVNYQlZkQzloYzNFeGFsQXJibXA1TTNOc2VVZEtaVVJSYjJzeGJtTTlJZ289fHcvtuKUEHDwZkp-cYkPzQIyxcOmtdI25whYIpmVBY35; __stripe_mid=a0406219-17a8-4adf-9b7d-52ae1bf4fbf8a70bec; auth=MTY2MjAwODg5OXxEdi1CQkFFQ180SUFBUkFCRUFBQVpfLUNBQU1HYzNSeWFXNW5EQThBRFdGMWRHaGxiblJwWTJGMFpXUUVZbTl2YkFJQ0FBRUdjM1J5YVc1bkRBa0FCM1Z6WlhKZmFXUUdkV2x1ZERZMEJnVUFfUUV1S0FaemRISnBibWNNRGdBTWMzVmljMk55YVhCMGFXOXVCbk4wY21sdVp3d0NBQUE9fJ9PRAjyiaMHzj9nxuGeY-JWtdWbwp-6kdXKvxxnVhbR',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
    }
    try:
        while True:
            req = requests.get(url, headers=headers, timeout=(5, 3))
            if req.status_code != 200:
                logger.error(f'{url} is unrechable,10s后尝试重连')
                time.sleep(10)
                continue
            logger.info(f'{url} connect success')
            bs = BeautifulSoup(req.text, 'lxml')
            tmp = bs.select(
                'body > main > div > div:nth-child(2) > div.col-lg-8.px-lg-2.my-2 > div > div.d-flex.flex-column.justify-content-center > div.overview-container.d-flex.flex-wrap.justify-content-center > div:nth-child(4) > span.text-success')
            validator_effectiveness = int(tmp[0].get_text().split('-')[0].strip().strip('%'))
            tmp = bs.select(
                'body > main > div > div:nth-child(2) > div.col-lg-8.px-lg-2.my-2 > div > div.d-flex.flex-column.justify-content-center > div.overview-container.d-flex.flex-wrap.justify-content-center > div:nth-child(3) > b')
            validator_status = 0
            if tmp[0].get_text() != 'Active':
                validator_status = 1
            obol_labels['validator_effectiveness'] = validator_effectiveness
            obol_labels['validator_status'] = validator_status
            if len(obol_labels) != 2:
                logger.error('get obol label failed!')
                return 'get obol label failed!'
            logger.info('get obol label success')
            return obol_labels
    except Exception as e:
        logger.error(e)
    finally:
        req.close()


if __name__ == '__main__':
    # gauge = Gauge('obol_monitor', 'Obol custom monitor about business', ['label_name'])
    # start_http_server(9033)
    # while True:
    #     labels = get_label(prefix_url,validator_index_list[0])
    #
    #     for k,v in labels.items():
    #         gauge.labels(k).set(v)
    #
    try:
        start_http_server(9033)
        gauge_validator_effectiveness = Gauge('validator_effectiveness', 'Obol custom monitor about business')
        gauge_validator_status = Gauge('validator_status', 'Obol custom monitor about business')

        while True:
            labels = get_label(prefix_url, validator_index_list[0])
            gauge_validator_effectiveness.set(labels['validator_effectiveness'])
            gauge_validator_status.set(labels['validator_status'])
            time.sleep(300)

    except Exception as e:
        logger.exception(e)
