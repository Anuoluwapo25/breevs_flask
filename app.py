from flask import Flask, request, Response
import requests
import os

app = Flask(__name__)

BOT_TOKEN = 'TELEGRAM_BOT_TOKEN'
WEBHOOK_URL = 'https://breevs-flask.onrender.com/webhook'

def setup_webhook():
    """Setup webhook for Telegram bot"""
    setup_url = f'https://api.telegram.org/bot{BOT_TOKEN}/setWebhook'
    response = requests.post(setup_url, json={'url': WEBHOOK_URL})
    if response.status_code == 200:
        print("Webhook setup successful")
        return response.json()
    print("Webhook setup failed")
    return response.json()

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming updates from Telegram"""
    if request.method == 'POST':
        # Parse the update
        update = request.get_json()
        
        # Check if we received a message
        if 'message' in update:
            chat_id = update['message']['chat']['id']
            
            # Check if the message contains text
            if 'text' in update['message']:
                message_text = update['message']['text']
                
                # Example: Echo the received message back
                send_message(chat_id, f"You said: {message_text}")
        
        return Response('ok', status=200)
    
    return Response(status=403)

def send_message(chat_id, text):
    """Send message back to Telegram"""
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    requests.post(url, json=payload)

if __name__ == '__main__':
    
    setup_webhook()
   
    app.run(host='0.0.0.0', port=5000, ssl_context='adhoc')