#!/usr/bin/env python
import requests
import re

from http.cookiejar import CookieJar
from typing import Optional
from urllib.parse import urlparse


HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}


class NotFound(Exception):
    pass


class InvalidValue(Exception):
    pass


def hostname(url: str) -> str:
    return urlparse(url).hostname


def add_host(headers: dict, url: str) -> dict:
    return {**headers, "Host": hostname(url)}


def fetch_headers(url: str, cookie_jar: Optional[CookieJar] = None) -> dict:
    """Return headers with lowercase keys"""
    resp = requests.get(
        url, headers=add_host(HEADERS, url), cookies=cookie_jar
    )
    if resp.status_code != 200:
        raise NotFound(url)
    return {k.lower(): v for k, v in resp.headers.items()}


class HSTSInfo:
    _max_age_pattern = re.compile(r".*max-age=(\d+)")

    def __init__(self, headers: dict):
        self._hsts_str = headers.get("strict-transport-security")

    @property
    def has_hsts(self) -> bool:
        return self._hsts_str is not None

    @property
    def max_age(self) -> Optional[int]:
        if self._hsts_str is not None:
            match = self._max_age_pattern.match(self._hsts_str)
            if match is not None:
                return int(match.group(1))
        return None

    @property
    def includes_subdomains(self) -> bool:
        if self._hsts_str is not None:
            return self._hsts_str.find("includeSubDomains") != -1
        return False


class CSPInfo:
    def __init__(self, headers: dict, host: str):
        self._csp_str = headers.get("content-security-policy")
        self._host = host

    @property
    def includes_subdomains(self) -> bool:
        if self._csp_str is not None:
            host = ".".join(self._host.split(".")[-2:])
            return self._csp_str.find(f".{host}") != -1
        return False


def main():
    pass


if __name__ == "__main__":
    # url = "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent/Firefox"
    # url = "https://www.facebook.com/"
    url = "https://fb.com"
    print(hostname(url))
    jar = CookieJar()
    headers = fetch_headers(url, jar)
    hsts_info = HSTSInfo(headers)
    print(hsts_info.has_hsts)
    print(hsts_info.includes_subdomains)
    print(hsts_info.max_age)
    csp_info = CSPInfo(headers, hostname(url))
    print(csp_info.includes_subdomains)
    print(csp_info._csp_str)
    # print(jar._cookies)
