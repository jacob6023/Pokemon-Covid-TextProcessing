import csv
from datetime import datetime
from collections import defaultdict

def calculate_average_age(age_range):
    if '-' in age_range:
        start, end = map(int, age_range.split('-'))
        return str(round((start + end) / 2))
    return age_range

def change_date_format(date_str):
    try:
        return datetime.strptime(date_str, '%d.%m.%Y').strftime('%m.%d.%Y')
    except ValueError:
        return date_str

def process_csv(input_file, output_file):
    data = []
    province_lat_long = defaultdict(lambda: {'lat': [], 'long': []})
    province_city_freq = defaultdict(lambda: defaultdict(int))
    province_symptom_freq = defaultdict(lambda: defaultdict(int))
    
    with open(input_file, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            #Normalize age
            row['age'] = calculate_average_age(row['age'])
            
            #Change date formats
            for date_field in ['date_onset_symptoms', 'date_admission_hospital', 'date_confirmation']:
                row[date_field] = change_date_format(row[date_field])
            
            #Check data for latitude/longitude averages and city/symptom frequencies
            if row['latitude'] != 'NaN' and row['longitude'] != 'NaN':
                province_lat_long[row['province']]['lat'].append(float(row['latitude']))
                province_lat_long[row['province']]['long'].append(float(row['longitude']))
            
            if row['city'] != 'NaN':
                province_city_freq[row['province']][row['city']] += 1
            
            if row['symptoms'] != 'NaN':
                symptoms = row['symptoms'].replace('; ', ';').split(';')
                for symptom in symptoms:
                    province_symptom_freq[row['province']][symptom.strip()] += 1
            
            data.append(row)
    
    #Compute averages and most frequent values
    for province, coords in province_lat_long.items():
        lat_avg = round(sum(coords['lat']) / len(coords['lat']), 2) if coords['lat'] else 'NaN'
        long_avg = round(sum(coords['long']) / len(coords['long']), 2) if coords['long'] else 'NaN'
        province_lat_long[province] = (lat_avg, long_avg)
    
    most_frequent_city = {province: max(cities, key=cities.get) for province, cities in province_city_freq.items()}
    most_frequent_symptom = {province: max(symptoms, key=symptoms.get) for province, symptoms in province_symptom_freq.items()}
    
    #Fill missing values and write to output
    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in data:
            if row['latitude'] == 'NaN' or row['longitude'] == 'NaN':
                row['latitude'], row['longitude'] = province_lat_long[row['province']]
            
            if row['city'] == 'NaN' and row['province'] in most_frequent_city:
                row['city'] = most_frequent_city[row['province']]
            
            if row['symptoms'] == 'NaN' and row['province'] in most_frequent_symptom:
                row['symptoms'] = most_frequent_symptom[row['province']]
            
            writer.writerow(row)

process_csv("covidTrain.csv", "covidResult.csv")
