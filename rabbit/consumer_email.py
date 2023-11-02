import pika
import json
from model import Contact
import signal
import sys


credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue='email_queue', durable=True)

print('[*] Waiting for message. To exit, press Ctrl+C')


def email_callback(ch: pika.channel.Channel, method: pika.spec.Basic.Deliver,
                   properties: pika.spec.BasicProperties, body: bytes) -> None:
    """
       Callback function to process incoming email messages.
       Args:
           ch: Channel
           method: Delivery method
           properties: Message properties
           body: Message body
     """
    contact_data = json.loads(body)
    contact_id = contact_data.get("contact_id")
    contact = Contact.objects(id=contact_id).first()

    if contact:
        contact.send = True
        contact.save()
        print(f"Sending email to {contact.email}...send.status: {contact.send}")

def exit_gracefully(signum: int, frame) -> None:
    """
     Gracefully exit the program.
     Args:
         signum: Signal number
         frame: Current stack frame
     """
    print("Exiting gracefully...")
    connection.close()
    sys.exit(0)

# Перехоплення сигналу Ctrl+C
signal.signal(signal.SIGINT, exit_gracefully)

channel.basic_consume(queue='email_queue', on_message_callback=email_callback)


if __name__ == '__main__':
    channel.start_consuming()



