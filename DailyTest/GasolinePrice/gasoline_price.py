import re
import logging
import datetime
import requests
from requests import request
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class GasolinePrice():
    pass

    def __init__(self, region: str):
        self._region = region

    def get_price(self):
        logger.info("update info from http://www.qiyoujiage.com/")

        gas_res = {}
        response = None
        header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
        }
        try:
            response = request('GET', 'http://www.qiyoujiage.com/' + self._region + '.shtml', headers=header)
            response.encoding = 'utf-8'
        except requests.exceptions.Timeout:
            logger.error("Request Time Out!!!")
        except requests.exceptions.RequestException:
            logger.error("Request Failed.")
        if response:
            soup = BeautifulSoup(response.text, "lxml")
            dls = soup.select("#youjia > dl")
            next_adjust = soup.select("#youjiaCont > div")[1].contents[0].strip()

            for dl in dls:
                k = re.search("\d+", dl.select('dt')[0].text).group()
                if k in ['95', '98']:
                    gas_res[k] = dl.select('dd')[0].text
            gas_res["update_time"] = datetime.datetime.now().strftime('%Y-%m-%d')
            gas_res["tips"] = soup.select("#youjiaCont > div:nth-of-type(2) > span")[0].text.strip()  # 油价涨跌信息
            gas_res["next_adjust"] = next_adjust

        return gas_res


gp = GasolinePrice(region='beijing')
res = gp.get_price()
print(res)
