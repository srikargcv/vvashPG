from flask import Flask, jsonify, request
import requests as r
import os

# Load credentials from environment variables
XClientSecret = os.getenv('X-Client-Secret')
XClientId = os.getenv('X-Client-Id')

app = Flask(__name__)

@app.route('/order/create', methods=['POST'])
def create_order():
    headers = {
        'X-Client-Secret': XClientSecret,
        'X-Client-Id': XClientId,
        'x-api-version': '2025-01-01',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    body = request.json

    # Validate required fields
    required_fields = ['order_amount', 'order_currency', 'customer_details']
    for field in required_fields:
        if field not in body:
            return jsonify({
                'valid': False,
                'responsedata': f'Missing required field: {field}'
            }), 400

    try:
        url = "https://sandbox.cashfree.com/pg/orders"
        orderdata = r.post(url, headers=headers, json=body)

        if orderdata.ok and orderdata.content:
            data = orderdata.json()
            # Return order_id and payment_session_id only
            return jsonify({
                'valid': True,
                'order_id': data.get('order_id'),
                'payment_session_id': data.get('payment_session_id'),
                'full_response': data
            })
        else:
            return jsonify({
                'valid': False,
                'responsedata': f"Failed: {orderdata.status_code} {orderdata.text}"
            }), orderdata.status_code

    except r.RequestException as e:
        return jsonify({
            'valid': False,
            'responsedata': f"Request error: {str(e)}"
        }), 500


@app.route('/order/status', methods=['POST'])
def get_order_status():
    content = request.json

    order_id = content.get("order_id")
    if not order_id:
        return jsonify({
            'valid': False,
            'responsedata': 'Missing required parameter: order_id'
        }), 400

    headers = {
        'X-Client-Secret': XClientSecret,
        'X-Client-Id': XClientId,
        'x-api-version': '2025-01-01',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    try:
        url = f"https://sandbox.cashfree.com/pg/orders/{order_id}"
        orderdata = r.get(url, headers=headers)

        if orderdata.ok and orderdata.content:
            return jsonify({
                'valid': True,
                'responsedata': orderdata.json()
            })
        else:
            return jsonify({
                'valid': False,
                'responsedata': f"Failed: {orderdata.status_code} {orderdata.text}"
            }), orderdata.status_code

    except r.RequestException as e:
        return jsonify({
            'valid': False,
            'responsedata': f"Request error: {str(e)}"
        }), 500

