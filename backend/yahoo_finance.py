import requests


def get_stock_price(stock_code):
    """
    从雅虎财经获取股票价格
    """
    url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={stock_code}"
    try:
        response = requests.get(url)
        data = response.json()
        return data['quoteResponse']['result'][0]['regularMarketPrice']
    except Exception as e:
        print(f"获取股票价格失败: {e}")
        return None