from flask import Flask, jsonify, request, render_template
from ib_gateway import submit_order, fetch_open_orders
from yahoo_finance import get_stock_price
from tasks import start_monitoring

app = Flask(__name__)

# 存储当前的委托单任务
orders = []


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/orders', methods=['GET'])
def get_orders():
    """
    返回所有委托单
    """
    return jsonify(orders), 200


@app.route('/api/orders', methods=['POST'])
def add_order():
    """
    添加新的委托单
    """
    data = request.json
    stock_code = data.get('stock_code')
    action = data.get('action')
    price = data.get('price')
    time_range = data.get('time_range')

    if not stock_code or not action or not price or not time_range:
        return jsonify({'error': '缺少必要参数'}), 400

    order = {
        'id': len(orders) + 1,
        'stock_code': stock_code,
        'action': action,
        'price': price,
        'time_range': time_range,
        'status': '未提交'
    }
    orders.append(order)
    start_monitoring(order)  # 启动监控任务
    return jsonify({'message': '委托单添加成功！', 'order': order}), 201


@app.route('/api/fetch_open_orders', methods=['GET'])
def fetch_orders():
    """
    从 IB Gateway 获取当前打开的委托单
    """
    open_orders = fetch_open_orders()
    return jsonify(open_orders), 200


if __name__ == '__main__':
    app.run(debug=True)