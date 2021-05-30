#!/usr/bin/python3
import requests
import time
from bs4 import BeautifulSoup
import config

def amazon_request(code):
    url = f"https://www.amazon.com.br/gp/product/{code}"
    print(f"Accessing {url}") 
    try:
        response = requests.get(
            url,
            #verify=False,
            headers={
                "authority": "www.amazon.com.br",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
                "accept-language": "en-US,en;q=0.9,pt;q=0.8",
            },
        )
    except requests.exceptions.RequestException as err:
        raise SystemExit(f"HTTP request failed: {err}")
    return response

def main():
    i = 0
    while True:
        i += 1
        print(f"[{i}] About to reach: {config.source} ({config.product})")
        r = amazon_request(config.product)
        if r.status_code == 200:
            break
        if i > 9:
            raise SystemExit("HTTP request failed due to timeout")
        time.sleep(1)

    try:
        soup = BeautifulSoup(r.content, "html.parser")
        price = soup.find_all("span", {"class" : "p13n-sc-price"})[1]
        print(price.text)
    except IndexError as err:
        raise SystemExit(f"Object was not found: {err}")
    print("DONE")

def handler(event, context):
    try:
        print(f"Log: {context.log_group_name}")
        print(f"Param: {event}")
        config.source = event["source"]
        config.product = event["code"]
    except KeyError as err:
        raise SystemExit(f"Missing parameters, check the payload: {err}")
    main()

if __name__ == "__main__":
    main()
