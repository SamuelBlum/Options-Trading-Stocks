import boto3
import argparse

def main(args):

    access_key = ''
    secret_key = ''

    # Get the service resource
    sqs = boto3.resource('sqs', region_name='us-east-2', aws_access_key_id=access_key, aws_secret_access_key=secret_key)

    if args.create_queue == True:
        create_queue(sqs)
    if args.list_queues == True:
        list_queues(sqs)
    if args.receive_queue == True:
        receive_queue(sqs)
    if args.send_queue == True:
        send_queue(sqs, args.message)
    if args.send_sns == True:
        send_sns(args.phone_number, args.message, access_key, secret_key)

def create_queue(sqs):
    # Create the queue
    queue = sqs.create_queue(QueueName='test', Attributes={'DelaySeconds': '5'})
    # Print queue attributes
    print(queue.url)
    print(queue.attributes.get('DelaySeconds'))

def list_queues(sqs):
    for queue in sqs.queues.all():
        print(queue.url)

def receive_queue(sqs):
    # Get the queue
    queue = sqs.get_queue_by_name(QueueName='test')
    # Process messages by printing out body and optional author name
    for message in queue.receive_messages(MessageAttributeNames=['Author']):
        # Get the custom author message attribute if it was set
        author_text = ''
        if message.message_attributes is not None:
            author_name = message.message_attributes.get('Author').get('StringValue')
            if author_name:
                author_text = ' ({0})'.format(author_name)
        # Print out the body and author (if set)
        print(message.body)
        # Let the queue know that the message is processed
        message.delete()

def send_queue(sqs, message):

    # Get the queue
    queue = sqs.get_queue_by_name(QueueName='test')
    # Create a new message
    response = queue.send_message(MessageBody=message)
    # Print Message ID and MD5
    print(response.get('MessageId'))
    print(response.get('MD5OfMessageBody'))


def send_sns(phone_number, message, access_key, secret_key):

    # Create SNS client
    client = boto3.client(
        "sns",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name="us-east-1"
    )

    # Send sms message.
    client.publish(
        PhoneNumber=phone_number,
        Message=message
    )

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--create_queue', default=False, type=bool) 
    parser.add_argument('--list_queues', default=False, type=bool) 
    parser.add_argument('--receive_queue', default=False, type=bool) 
    parser.add_argument('--send_queue', default=False, type=bool) 
    parser.add_argument('--send_sns', default=False, type=bool) 
    parser.add_argument('--message', default='test', type=str) 
    parser.add_argument('--phone_number', default='+14438448537', type=str) 

    args = parser.parse_args()
    
    main(args)
    

