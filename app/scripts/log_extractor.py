import win32evtlog
import requests

SERVER = None  # None specifies the local machine
LOG_TYPE = "Security"
BASE_URL = "http://localhost:8000/api/v1/logs"

hand = win32evtlog.OpenEventLog(SERVER, LOG_TYPE)
flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ

session = requests.Session()

try:
    while True:
        events = win32evtlog.ReadEventLog(hand, flags, 0)
        if not events:
            break

        for event in events:
            event_id = event.EventID & 0xFFFF

            if event_id not in (4624, 4625):
                continue

            payload = {
                "event_id": event_id,
                "time": str(event.TimeGenerated),
                "inserts": list(event.StringInserts) if event.StringInserts else []
            }

            print(payload)
            endpoint = f"{BASE_URL}/failed_login" if event_id == 4625 else f"{BASE_URL}/successful_login"
            
            # try:
            #     resp = session.post(endpoint, json=payload, timeout=5)
            #     resp.raise_for_status()
            # except requests.RequestException as e:
            #     print(f"Failed to send event {event_id}: {e}")

finally:
    session.close()
    win32evtlog.CloseEventLog(hand)
