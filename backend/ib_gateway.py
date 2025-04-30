from ib_insync import IB, Stock, MarketOrder


def connect_to_ib():
    """
    连接到 IB Gateway 或 TWS
    """
    ib = IB()
    try:
        ib.connect('127.0.0.1', 4002, clientId=1)
        print("成功连接到 IB Gateway")
        return ib
    except Exception as e:
        print(f"连接失败: {e}")
        return None


def submit_order(stock_code, action, quantity, price):
    """
    提交订单到 IB Gateway
    """
    ib = connect_to_ib()
    if not ib:
        return {'error': '无法连接到 IB Gateway'}

    try:
        stock = Stock(stock_code, 'SMART', 'USD')
        ib.qualifyContracts(stock)
        order_type = 'BUY' if action == '买入' else 'SELL'
        order = MarketOrder(order_type, quantity)
        trade = ib.placeOrder(stock, order)
        ib.sleep(1)
        print(f"委托单提交成功: {trade}")
        return {'status': '提交', 'trade': trade}
    except Exception as e:
        print(f"提交订单失败: {e}")
        return {'error': str(e)}
    finally:
        ib.disconnect()


def fetch_open_orders():
    """
    获取当前打开的委托单
    """
    ib = connect_to_ib()
    if not ib:
        return {'error': '无法连接到 IB Gateway'}

    try:
        open_orders = ib.reqOpenOrders()
        return [{'orderId': o.orderId, 'status': o.status} for o in open_orders]
    except Exception as e:
        print(f"查询打开的委托单失败: {e}")
        return {'error': str(e)}
    finally:
        ib.disconnect()