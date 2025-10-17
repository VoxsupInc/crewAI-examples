import os
from crewai.tools import tool
from sec_api import QueryApi
import requests
import html2text
import re


@tool("Search SEC 10-K filing")
def SEC10KTool(stock_ticker: str) -> str:
    """Fetches and returns the full text content of the latest 10-K SEC filing for a given stock ticker."""
    try:
        queryApi = QueryApi(api_key=os.environ['SEC_API_API_KEY'])
        query = {
            "query": {
                "query_string": {
                    "query": f"ticker:{stock_ticker} AND formType:\"10-K\""
                }
            },
            "from": "0",
            "size": "1",
            "sort": [{ "filedAt": { "order": "desc" }}]
        }
        filings = queryApi.get_filings(query)['filings']
        if len(filings) == 0:
            return f"No 10-K filings found for ticker {stock_ticker}."

        url = filings[0]['linkToFilingDetails']
        
        headers = {
            "User-Agent": "crewai.com bisan@crewai.com",
            "Accept-Encoding": "gzip, deflate",
            "Host": "www.sec.gov"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        h = html2text.HTML2Text()
        h.ignore_links = False
        text = h.handle(response.content.decode("utf-8"))

        text = re.sub(r"[^a-zA-Z$0-9\s\n]", "", text)
        max_length = 50000
        if len(text) > max_length:
            text = text[:max_length] + f"\n\n[Document truncated to {max_length} characters]"
        return text
    except requests.exceptions.HTTPError as e:
        return f"HTTP error occurred while fetching 10-K: {e}"
    except Exception as e:
        return f"Error fetching 10-K for {stock_ticker}: {e}"


@tool("Search SEC 10-Q filing")
def SEC10QTool(stock_ticker: str) -> str:
    """Fetches and returns the full text content of the latest 10-Q SEC filing for a given stock ticker."""
    try:
        queryApi = QueryApi(api_key=os.environ['SEC_API_API_KEY'])
        query = {
            "query": {
                "query_string": {
                    "query": f"ticker:{stock_ticker} AND formType:\"10-Q\""
                }
            },
            "from": "0",
            "size": "1",
            "sort": [{ "filedAt": { "order": "desc" }}]
        }
        filings = queryApi.get_filings(query)['filings']
        if len(filings) == 0:
            return f"No 10-Q filings found for ticker {stock_ticker}."

        url = filings[0]['linkToFilingDetails']
        
        headers = {
            "User-Agent": "crewai.com bisan@crewai.com",
            "Accept-Encoding": "gzip, deflate",
            "Host": "www.sec.gov"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        h = html2text.HTML2Text()
        h.ignore_links = False
        text = h.handle(response.content.decode("utf-8"))

        text = re.sub(r"[^a-zA-Z$0-9\s\n]", "", text)
        max_length = 50000
        if len(text) > max_length:
            text = text[:max_length] + f"\n\n[Document truncated to {max_length} characters]"
        return text
    except requests.exceptions.HTTPError as e:
        return f"HTTP error occurred while fetching 10-Q: {e}"
    except Exception as e:
        return f"Error fetching 10-Q for {stock_ticker}: {e}"

