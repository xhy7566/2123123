import time
from threading import Thread
from yahoo_finance import get_stock_price
from ib_gateway import submit_order


def monitor_order(order):
    """
    持续监控委托单是否满足条件
    """
    while order['status'] == '未提交':
        stock_price = get_stock_price(order['stock_code'])
        if stock_price is None:
            time.sleep(30)
            continue

        if order['action'] == '买入' and stock_price >= order['price']:
            submit_order(order['stock_code'], '买入', 1, stock_price)
            order['status'] = '提交'
        elif order['action'] == '卖出' and stock_price <= order['price']:
            submit_order(order['stock_code'], '卖出', 1, stock_price)
            order['status'] = '提交'

        time.sleep(30)


def start_monitoring(order):
    """
    启动监控任务
    """
    thread = Thread(target=monitor_order, args=(order,))
    thread.daemon = True
    thread.start()