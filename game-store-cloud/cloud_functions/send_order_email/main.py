import functions_framework
from flask import jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

@functions_framework.http
def send_order_email(request):
    """
    HTTP Cloud Function to send order confirmation email.
    
    This is a demo function that simulates sending emails.
    In production, you'd use SendGrid, Mailgun, or Gmail API.
    """
    
    # Parse request
    request_json = request.get_json(silent=True)
    
    if not request_json:
        return jsonify({'error': 'No data provided'}), 400
    
    email = request_json.get('email')
    order_id = request_json.get('order_id')
    total = request_json.get('total')
    items = request_json.get('items', [])
    
    if not email or not order_id:
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Simulate email sending (in production, use a real email service)
    print(f"Sending order confirmation to {email}")
    print(f"Order ID: {order_id}")
    print(f"Total: £{total}")
    print(f"Items: {items}")
    
    # Create email content
    email_body = f"""
    Thank you for your order!
    
    Order Number: #{order_id}
    Total Amount: £{total}
    
    Items Ordered:
    {format_items(items)}
    
    You will receive download links shortly.
    
    Thank you for shopping with Game Store!
    """
    
    # In production, you would actually send the email here
    # For now, we'll just log it
    
    return jsonify({
        'success': True,
        'message': f'Order confirmation email sent to {email}',
        'order_id': order_id
    }), 200

def format_items(items):
    """Format items list for email"""
    if not items:
        return "No items"
    
    formatted = []
    for item in items:
        formatted.append(f"- {item.get('title', 'Unknown')} x{item.get('quantity', 1)}")
    
    return '\n'.join(formatted)
