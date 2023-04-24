from bs4 import BeautifulSoup
import requests
import asyncio
import aiohttp
from fake_useragent import FakeUserAgent
from pprint import pprint


class GetValidatedProxy:

    def __init__(self):
        self.site_with_free_proxies: str = 'https://free-proxy-list.net'
        self.good_proxies: list[str] = []

    def get_soup(self) -> BeautifulSoup:
        return BeautifulSoup(requests.get(self.site_with_free_proxies).text, 'lxml')

    def get_proxies(self) -> list[str]:
        proxies: list[str] = []
        soup: BeautifulSoup = self.get_soup()
        table: list = soup.select_one('.table-striped tbody').find_all('tr')
        for row in table:
            if row.select_one('td:nth-child(7)').text == 'yes' and (
                    row.select_one('td:nth-child(5)').text == 'anonymous' or row.select_one(
                    'td:nth-child(5)').text == 'elite proxy'):
                proxy: str = row.findNext().text + ':' + row.findNext().findNext().text
                if len(proxies) >= 10:  # MANUAL REGULATION OF PROXY QUANTITY
                    break
                proxies.append(proxy)
        return proxies

    async def get_validated_proxy(self, proxy, session):
        url_for_testing_proxy: str = 'http://httpbin.org/ip'
        try:
            async with session.get(url=url_for_testing_proxy, proxy=proxy) as response:
                if response.ok:
                    print(f'good proxy, status_code -{response.status}-', proxy)
                    self.good_proxies.append(proxy)
        except Exception as _ex:
            pass

    async def run_script(self):
        headers = {'user-agent': FakeUserAgent().random}
        async with aiohttp.ClientSession(headers=headers) as session:
            tasks = [asyncio.create_task(self.get_validated_proxy(f'http://{prx}', session)) for prx in
                     self.get_proxies()]
            await asyncio.gather(*tasks)

    @staticmethod
    async def main():
        pr = GetValidatedProxy()
        await pr.run_script()
        pprint(pr.good_proxies)
        return pr.good_proxies

