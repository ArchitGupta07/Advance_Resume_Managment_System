# import sys, types
# from 'kafka.vendor.six.moves' import queue 

# m = types.ModuleType('kafka.vendor.six.moves', 'Mock module')
# # setattr(m, 'range', range)
# # sys.modules['kafka.vendor.six.moves'] = m

# if sys.version_info >= (3,12,0): sys.modules['kafka.vendor.six.moves'] = m
import traceback
from kafka import KafkaConsumer
import json
import spacy
from parser.main_func import main
import requests
from minioClient import client
from datetime import timedelta

def downloadFile(filename):
    url = client.get_presigned_url(
        "GET",
        "armss-dev",
        filename,
        expires=timedelta(days=1),
    )
    print(url)
    return url


def handleUpload(filename):
    url = downloadFile(filename)
    main(url)


def consumer_function():
    # Initialize Kafka consumer
    consumer = KafkaConsumer('resumePoster', bootstrap_servers=['kafka:9092'],
                            value_deserializer=lambda x: json.loads(x.decode('utf-8')))
    
    print(consumer)

    try:
        # Start consuming messages
        for msg in consumer:
            # Access individual fields from JSON data
            # filename = msg.value.get('name')
            # filepath = msg.value.get('path')
            # created_at = msg.value.get('created_at')
            # print(f"name: {filename}, path: {filepath}, Created At: {created_at}")
            print(msg)
            filename = msg.value["Key"].split("/")[-1]
            handleUpload(filename)
            # fileJson = {
            #     'filename':filename,
            #     'filepath':filepath,
            #     'created_at':created_at
            # }
            # printThis();
            # print(main(filepath))
            # callApi(fileJson)
    except Exception as e:
        traceback.print_exc()

        print(f"Error: {e}")
    finally:
        # Close the consumer
        consumer.close()



    
# handleUpload('jS')



