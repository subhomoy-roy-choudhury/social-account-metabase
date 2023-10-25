from __future__ import absolute_import, unicode_literals
import requests
import json
from celery import shared_task
from datetime import datetime

@shared_task(name = "print_msg_main")
def print_message(message, *args, **kwargs):
  print(f"Celery is working!! Message is {message}")

@shared_task(name = "print_time")
def print_time():
  now = datetime.now()
  current_time = now.strftime("%H:%M:%S")
  print(f"Current Time is {current_time}")
  
@shared_task(name='get_calculation')
def calculate(val1, val2):
  total = val1 + val2
  return total

@shared_task(name='post_webhook')
def send_linkedin_post():
    url = "https://webhook-test.com/2daa4106c85d94eb9acb9bce18082662"

    payload = json.dumps({
    "username": "xyz123",
    "password": "xyz"
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    # print("Send Linkedin Post")