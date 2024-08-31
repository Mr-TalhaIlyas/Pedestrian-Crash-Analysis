import requests
import time
import xml.etree.ElementTree as ET
from openpyxl import Workbook
from datetime import datetime, timedelta

def fetch_data_from_api():
    # URL dell'API con i parametri richiesti
    url = 'https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/xml'
    params = {
        'key': 'w3OSvxEyuS95ygBGPt6Co0MktJcOVWms',
        'point': '38.1042,13.33306'
    }

    response = requests.get(url, params=params) 
    if response.status_code == 200:
        # Analizza il contenuto XML della risposta
        root = ET.fromstring(response.content)
        # Estrai gli attributi richiesti
        frc = root.find('.//frc').text if root.find('.//frc') is not None else 'N/A'
        current_speed = root.find('.//currentSpeed').text if root.find('.//currentSpeed') is not None else 'N/A'
        free_flow_speed = root.find('.//freeFlowSpeed').text if root.find('.//freeFlowSpeed') is not None else 'N/A'
        current_travel_time = root.find('.//currentTravelTime').text if root.find('.//currentTravelTime') is not None else 'N/A'
        free_flow_travel_time = root.find('.//freeFlowTravelTime').text if root.find('.//freeFlowTravelTime') is not None else 'N/A'
        typical_speed = root.find('.//typicalSpeed').text if root.find('.//typicalSpeed') is not None else 'N/A'
        confidence = root.find('.//confidence').text if root.find('.//confidence') is not None else 'N/A'
        print(datetime.now().strftime('%Y/%m/%d %H:%M:%S'), frc, current_speed, free_flow_speed, current_travel_time, free_flow_travel_time, typical_speed, confidence)
        # Ritorna i dati
        return [datetime.now().strftime('%Y/%m/%d %H:%M:%S'), frc, current_speed, free_flow_speed, current_travel_time, free_flow_travel_time, typical_speed, confidence]
    else:
        print("Errore nella richiesta all'API.")
        return None

def save_data_to_excel(data, filename):
    # Crea un nuovo workbook
    workbook = Workbook()
    sheet = workbook.active

    # Assegna un titolo alle colonne
    headers = ["YYYY/MM/DD HH:MM:SS", "FRC", "Current Speed", "Free Flow Speed", "Current Travel Time", "Free Flow Travel Time", "Typical Speed",  "Confidence"]
    sheet.append(headers)

    # Aggiungi i dati alla sheet
    for row in data:
        sheet.append(row)

    # Salva il workbook nel file Excel
    workbook.save(filename)

def main():
    filename = '/home/user01/Data/roads/data_table.xlsx'
    collected_data = []
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=24)
    SLEEPING_TIME = 300  # 5 minutes in seconds

    while datetime.now() <= end_time:
        data = fetch_data_from_api()
        if data:
            collected_data.append(data)
        save_data_to_excel(collected_data, filename)
        time.sleep(SLEEPING_TIME)

if __name__ == "__main__":
    main()
