from googleapiclient.discovery import build
import pickle
import json

with open('token.pickle', 'rb') as token_file:
    creds = pickle.load(token_file)

service = build('calendar', 'v3', credentials=creds)

# Load calendar IDs from your config.json
with open("config.json", "r") as f:
    config = json.load(f)

target_calendar_id = config["target_calendar_id"]

# Delete all events from target calendar (CAREFUL!)
events = service.events().list(calendarId=target_calendar_id).execute().get('items', [])

for event in events:
    print(f"Deleting event: {event['summary']}")
    service.events().delete(calendarId=target_calendar_id, eventId=event['id']).execute()

print("Calendar cleared.")
