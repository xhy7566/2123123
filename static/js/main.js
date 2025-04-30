document.getElementById('addOrder').addEventListener('click', () => {
    const stockCode = document.getElementById('stockCode').value;
    const timeRange = document.getElementById('timeRange').value;
    const action = document.getElementById('action').value;
    const price = document.getElementById('price').value;

    fetch('/api/orders', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ stock_code: stockCode, action, time_range: timeRange, price: parseFloat(price) })
    }).then(response => response.json())
      .then(data => {
          alert(data.message || data.error);
          loadOrders();
      });
});

function loadOrders() {
    fetch('/api/orders').then(response => response.json()).then(data => {
        const orderList = document.getElementById('orderList');
        orderList.innerHTML = '';
        data.forEach(order => {
            const row = `<tr>
                <td>${order.id}</td>
                <td>${order.stock_code}</td>
                <td>${order.action}</td>
                <td>${order.price}</td>
                <td>${order.status}</td>
            </tr>`;
            orderList.innerHTML += row;
        });
    });
}

loadOrders();