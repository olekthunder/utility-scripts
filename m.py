#!/usr/bin/env python
import platform
import re
import textwrap
from datetime import timedelta
from typing import Dict, Optional
from urllib.parse import urlparse

import requests

IS_WINDOWS = platform.system() == "Windows"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Linux; Android 6.0.1; E6653 Build"
        "/32.2.A.0.253) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/52.0.2743.98 Mobile Safari/537.36"
    ),
    "Accept": "*/*",
    "Accept-Encoding": "gzip",
    "Connection": "keep-alive",
}


class InvalidValue(Exception):
    pass


def hostname(url: str) -> str:
    return urlparse(url).hostname


def add_host(headers: dict, url: str) -> dict:
    return {**headers, "Host": hostname(url)}


def get(url, session: Optional[requests.Session] = None) -> requests.Response:
    if session is None:
        session = requests.Session()
    return session.get(url, headers=add_host(HEADERS, hostname(url)))


def fetch_headers(response: requests.Response) -> dict:
    """Return headers with lowercase keys"""
    return {k.lower(): v for k, v in response.headers.items()}


class HSTSInfo:
    _max_age_pattern = re.compile(r".*max-age=(\d+)")

    def __init__(self, headers: dict):
        self.header_string = headers.get("strict-transport-security")

    @property
    def enabled(self) -> bool:
        return self.header_string is not None

    @property
    def max_age(self) -> timedelta:
        if self.header_string is not None:
            match = self._max_age_pattern.match(self.header_string)
            if match is not None:
                return timedelta(seconds=int(match.group(1)))
        return timedelta(seconds=0)

    @property
    def includes_subdomains(self) -> bool:
        if self.header_string is not None:
            return self.header_string.find("includeSubDomains") != -1
        return False


class CSPInfo:
    awailable_directives = {
        "default-src",
        "script-src",
        "style-src",
        "img-src",
        "connect-src",
        "font-src",
        "object-src",
        "media-src",
        "frame-src",
        "sandbox",
        "report-uri",
        "child-src",
        "form-action",
        "frame-ancestors",
        "plugin-types",
        "base-uri",
    }

    _directive_re = re.compile(r"(?P<directive>\S+) (?P<value>.+)")

    def __init__(self, headers: dict, host: str):
        self.header_string = headers.get("content-security-policy")
        self._host = host

    @property
    def enabled(self) -> bool:
        return self.header_string is not None

    @property
    def includes_subdomains(self) -> bool:
        if self.header_string is not None:
            host = ".".join(self._host.split(".")[-2:])
            return self.header_string.find(f".{host}") != -1
        return False

    @property
    def directives(self) -> Dict[str, str]:
        directives_ = {}
        if self.header_string is not None:
            chunks = [
                chunk.strip()
                for chunk in self.header_string.rstrip("; \t").split(";")
            ]
            for chunk in chunks:
                parsed = self._directive_re.match(chunk)
                if not parsed:
                    raise InvalidValue(f"Bad directive string {chunk}")
                directive = parsed.group("directive")
                if directive not in self.awailable_directives:
                    raise InvalidValue(f"Unknown directive: {directive}")
                directives_[directive] = parsed.group("value")
        return directives_


class CookieInfo:
    def __init__(self, headers: dict):
        self.header_string = headers.get("set-cookie")

    @property
    def enabled(self) -> bool:
        return self.header_string is not None

    @property
    def has_secure_flag(self) -> bool:
        if self.header_string is not None:
            chunks = [
                chunk.strip()
                for chunk in self.header_string.rstrip("; \t").split(";")
            ]
            for chunk in chunks:
                if chunk == "secure":
                    return True
        return False


def bold(text: str) -> str:
    return text if IS_WINDOWS else f"\033[1m{text}\033[0m"


def yellow(text: str) -> str:
    return text if IS_WINDOWS else f"\033[1;33m{text}\033[0m"


def green(text: str) -> str:
    return text if IS_WINDOWS else f"\033[1;32m{text}\033[0m"


def red(text: str) -> str:
    return text if IS_WINDOWS else f"\033[1;31m{text}\033[0m"


def pretty_print(
    host,
    headers: dict,
    hsts_info: Optional[HSTSInfo] = None,
    csp_info: Optional[CSPInfo] = None,
    cookie_info: Optional[CookieInfo] = None,
) -> None:

    NO = red(bold("no"))
    YES = green(bold("yes"))
    print("*" * 80)
    print(f"Parsing result for {host}")

    print()
    print("RESPONSE HEADERS".center(80, "-"))
    for header, value in headers.items():
        print(textwrap.fill(f"{yellow(bold(header))}: {value}", 80))

    if hsts_info is not None:
        print("HSTS INFO".center(80, "-"))
        enabled = hsts_info.enabled
        print(f"HSTS enabled: {YES if enabled else NO}")
        if enabled:
            print(
                f"Max age: {int(hsts_info.max_age.total_seconds())} seconds "
                f"({hsts_info.max_age.days} days)"
            )
            print(
                f"Includes subdomains: "
                f"{YES if hsts_info.includes_subdomains else NO}"
            )

    if csp_info is not None:
        print("CSP INFO".center(80, "-"))
        enabled = csp_info.enabled
        print(f"CSP enabled: {YES if enabled else NO}")
        if enabled:
            print(
                textwrap.fill(
                    f"Found directives: {', '.join(csp_info.directives.keys())}",
                    width=80,
                )
            )

            print(
                f"Includes subdomains: "
                f"{YES if csp_info.includes_subdomains else NO}"
            )

    if cookie_info is not None:
        print("Cookie INFO".center(80, "-"))
        enabled = cookie_info.enabled
        print(f"Cookies enabled: {YES if enabled else NO}")
        if enabled:
            print(
                f"Secure flag enabled: "
                f"{YES if cookie_info.has_secure_flag else NO}"
            )
    print("*" * 80, end="\n\n\n")


def main():
    urls = [
        "https://fb.com",
        "https://korrespondent.net",
        "https://censor.net.ua",
        "https://microsoft.com",
        "https://gmail.com",
        "https://ukr.net",
        "https://google.com",
        "https://www.bbc.com/",
        "https://linkedin.com",
        "https://kpi.ua",
    ]
    session = requests.Session()
    for url in urls:
        response = get(url, session)
        headers = fetch_headers(response)
        host = hostname(url)
        pretty_print(
            headers=response.headers,
            host=host,
            hsts_info=HSTSInfo(headers),
            csp_info=CSPInfo(headers, host),
            cookie_info=CookieInfo(headers),
        )


if __name__ == "__main__":
    main()
