#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Dieses Skript prüft Google-Kalender nach Ereignissen, die "Phil" enthalten
und überträgt diese in einen anderen Google-Kalender.
Gedacht für stündliche Ausführung über einen Cronjob.
"""

import os
import json
import datetime
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Wenn du das Skript änderst, musst du eventuell den Umfang der Berechtigungen ändern
SCOPES = ['https://www.googleapis.com/auth/calendar']

def load_config():
    try:
        with open('config.json', 'r') as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        # Standardwerte oder leere Werte
        return {
            "source_calendar_id": "primary",
            "target_calendar_id": "your_target_calendar_id@group.calendar.google.com",
            "processed_events_file": "processed_events.pkl"
        }

# Konfiguration laden
config = load_config()

# Kalender-IDs aus der Konfiguration verwenden
SOURCE_CALENDAR_ID = config.get("source_calendar_id")
TARGET_CALENDAR_ID = config.get("target_calendar_id")
# Datei zum Speichern bereits übertragener Ereignisse
PROCESSED_EVENTS_FILE = config.get("processed_events_file")

def get_google_calendar_service():
    """Google Calendar API authentifizieren und Service erstellen."""
    creds = None
    # Token aus der Datei token.pickle laden, falls vorhanden
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # Wenn keine gültigen Anmeldedaten verfügbar sind, den Benutzer anmelden lassen
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Speichern der Anmeldedaten für die nächste Ausführung
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds)

def load_processed_events():
    """Lädt die Liste der bereits verarbeiteten Ereignisse."""
    if os.path.exists(PROCESSED_EVENTS_FILE):
        with open(PROCESSED_EVENTS_FILE, 'rb') as f:
            return pickle.load(f)
    return set()

def save_processed_events(processed_events):
    """Speichert die Liste der verarbeiteten Ereignisse."""
    with open(PROCESSED_EVENTS_FILE, 'wb') as f:
        pickle.dump(processed_events, f)

def main():
    # Calendar Service erstellen
    service = get_google_calendar_service()
    
    # Anfangs- und Enddatum für das aktuelle Jahr festlegen
    now = datetime.datetime.utcnow()
    start_of_year = datetime.datetime(now.year, 1, 1, 0, 0, 0).isoformat() + 'Z'
    end_of_year = datetime.datetime(now.year, 12, 31, 23, 59, 59).isoformat() + 'Z'
    
    # Bereits verarbeitete Ereignisse laden
    processed_events = load_processed_events()
    
    # Ereignisse im Quellkalender abrufen, die "Phil" enthalten
    print(f"Suche nach Ereignissen mit 'Phil' im Kalender für das Jahr {now.year}...")
    events_result = service.events().list(
        calendarId=SOURCE_CALENDAR_ID,
        timeMin=start_of_year,
        timeMax=end_of_year,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])
    
    if not events:
        print('Keine Ereignisse mit "Phil" gefunden.')
        return
    
    # Zähler für neu übertragene Ereignisse
    new_events_count = 0
    
    # Durch die Ereignisse iterieren und übertragen, wenn sie "Phil" enthalten
    for event in events:
        event_id = event['id']
        summary = event.get('summary', '')
        
        # Überprüfen, ob "Phil" im Titel enthalten ist und das Ereignis noch nicht verarbeitet wurde
        if 'phil' in summary.lower() and event_id not in processed_events:
            print(f"Übertrage Ereignis: {summary}")
            
            # Ereignis in den Zielkalender kopieren
            new_event = {
                'summary': event.get('summary'),
                'location': event.get('location', ''),
                'description': event.get('description', ''),
                'start': event.get('start'),
                'end': event.get('end'),
                'reminders': event.get('reminders', {})
            }
            
            # Erstellen des Ereignisses im Zielkalender
            created_event = service.events().insert(
                calendarId=TARGET_CALENDAR_ID,
                body=new_event
            ).execute()
            
            # Ereignis als verarbeitet markieren
            processed_events.add(event_id)
            new_events_count += 1
    
    # Verarbeitete Ereignisse speichern
    save_processed_events(processed_events)
    
    print(f"Fertig! {new_events_count} neue Ereignisse mit 'Phil' wurden übertragen.")

if __name__ == '__main__':
    main()