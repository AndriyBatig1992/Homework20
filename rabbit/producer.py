import pika
import json
import time
from bson import json_util
import random
from faker import Faker
from model import Contact

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='andriy', exchange_type='direct')
channel.queue_declare(queue='email_queue', durable=True)
channel.queue_declare(queue='sms_queue', durable=True)
channel.queue_bind(exchange='andriy',queue='email_queue')
channel.queue_bind(exchange='andriy',queue='sms_queue')

#
fake = Faker()


def main() -> None:
    """
       Main function to generate and send contact data to message queues.
    """
    Contact.objects().delete() #Видаляэмо старі контакти
    for i in range(10):
        name = fake.name()
        email = fake.email()
        send = False
        phone_number = fake.phone_number()
        preferred_notifications = random.choice(["SMS", "email"])
        contact = Contact(
            name=name,
            email=email,
            send=send,
            phone_number=phone_number,
            preferred_notifications=preferred_notifications
        )
        contact.save()

        contact_data = {
            "contact_id": str(contact.id),
            "name": contact.name,
            "email": contact.email,
            "send": contact.send,
            "phone_number": contact.phone_number,
            "preferred_notifications": contact.preferred_notifications
        }

        message = json.dumps(contact_data, default=json_util.default).encode()

        if contact.preferred_notifications == "SMS":
            contact.send = True
            contact.save()
            channel.basic_publish(
                exchange='andriy',
                routing_key='sms_queue',
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                ))
            print(" [x] Sent SMS to %r" % contact.name)
        elif contact.preferred_notifications == "email":
            contact.send = True
            contact.save()
            channel.basic_publish(
                exchange='andriy',
                routing_key='email_queue',
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                ))
            print(" [x] Sent email to %r" % contact.name)
            print("All messages sent. Waiting for consumers to finish...")
            time.sleep(3)


if __name__ == '__main__':
    main()


