import os
import django
import json
import sys
import smtplib
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from kafka import KafkaConsumer, TopicPartition
import heapq
import subprocess

# -----------------------------
# Setup Django environment
# -----------------------------
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "notify.settings")
django.setup()

from django.contrib.auth.models import User
from good.models import NotificationPreference
from notify import settings

# -----------------------------
# Kafka Topics and their Consumer Groups
# -----------------------------
TOPICS_GROUPS = {
    "first": "proj1",
    "second": "proj2",
    "third": "proj3",
    "fourth": "proj4",
}

# -----------------------------
# Email Configuration
# -----------------------------
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "dineshayadi584@gmail.com"
SENDER_PASSWORD = "hfkhrcwgvnuwhsnx"  # App password if 2FA enabled

def send_email(receiver_email, subject, body,messg):
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        print(f"Email sent to {receiver_email} {messg}")
    except Exception as e:
        print("Failed to send email:", e)

def send_sms(number, message):
    url = "https://api.msg91.com/api/sendhttp.php"
    params = {
        "authkey": settings.MSG91_AUTH_KEY,
        "mobiles": number,
        "message": message,
        "sender": settings.MSG91_SENDER_ID,
        "route": settings.MSG91_ROUTE,
        "country": "91"
    }
    # Implement actual request if needed

# -----------------------------
# Function to consume a single topic with priority
# -----------------------------
def consume_topic(topic, group_id):
    consumer = KafkaConsumer(
        bootstrap_servers="localhost:9092",
        group_id=group_id,
        auto_offset_reset="earliest",
        enable_auto_commit=False,  # manual commit for safety
        value_deserializer=lambda v: json.loads(v.decode("utf-8"))
    )

    # Assign all partitions manually
    partitions = consumer.partitions_for_topic(topic)
    topic_partitions = [TopicPartition(topic, p) for p in partitions]
    consumer.assign(topic_partitions)

    # Define partition priority: lower number = higher priority
    partition_priority = {0: 1, 1: 2, 2: 3, 3: 4}

    print(f"Consumer started for {topic} with group {group_id}")

    while True:
        messages = consumer.poll(timeout_ms=2000)
        queue = []

        for tp, msgs in messages.items():
            for msg in msgs:
                # Add messages to priority queue
                heapq.heappush(queue, (partition_priority.get(tp.partition, 999), tp.partition, msg.offset, msg))

        while queue:
            _, partition, offset, msg = heapq.heappop(queue)
            print(f"Processing partition {partition}, offset {offset}, message: {msg.value}")

            # Send notifications to subscribed users
            preferences = NotificationPreference.objects.filter(topic=topic)
            for pref in preferences:
                subject = f"New Notification from {topic}"
                body = f"Message received from {topic}:\n\n{json.dumps(msg.value, indent=2)}"
                if pref.method == "email":
                    send_email(pref.user.email, subject, body,msg.value)
                elif pref.method == "sms":
                    send_sms(pref.user.profile.phone, msg.value)
                    print(f"Would send SMS to {pref.user.username}")
                elif pref.method == "whatsapp":
                    print(f"Would send WhatsApp to {pref.user.username}")

            # Commit offset after processing
            consumer.commit()

# -----------------------------
# Start a consumer thread for each topic
# -----------------------------
threads = []
for topic, group_id in TOPICS_GROUPS.items():
    t = threading.Thread(target=consume_topic, args=(topic, group_id))
    t.start()
    threads.append(t)

for t in threads:
    t.join()


js_code = "console.log('Hello from JS inside Python!');"
subprocess.run(["node", "-e", js_code])