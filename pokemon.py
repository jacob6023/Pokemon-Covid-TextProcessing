import csv
from collections import Counter
from pathlib import Path


def method_1(f):
    fire_count = 0
    fire_above_level_40_count = 0

    with open(f, mode='r', newline='') as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            # Check if the Pokémon is of type "fire"
            if row['type'] == 'fire':
                fire_count += 1
                # Check if the Pokémon's level is at or above 40
                if row['level'] and float(row['level']) >= 40:
                    fire_above_level_40_count += 1

    # Calculate the percentage
    if fire_count > 0:
        percentage = (fire_above_level_40_count / fire_count) * 100
    else:
        percentage = 0

    # Round off the percentage using the round()
    percentage = round(percentage)
    file1 = open("pokemon1.txt", "a")
    file1.write(str(percentage))
    file1.close()        

    return percentage


def method_2(f):
    weakness_to_type_mapping = {
        'fighting': 'normal',
        'flying': 'bug',
        'poison': 'bug',
        'ground': 'rock',
        'rock': 'water',
        'bug': 'grass',
        'ghost': 'dark',
        'steel': 'fire',
        'fire': 'water',
        'water': 'grass',
        'grass': 'fire',
        'electric': 'water',
        'psychic': 'bug',
        'ice': 'fighting',
        'dragon': 'flying',
        'dark': 'fighting',
        'fairy': 'poison',
        'normal': 'fighting'
    }

    with open(f, mode='r', newline='') as file:
        csv_reader = csv.DictReader(file)
        data = list(csv_reader)

    # Count occurrences of types for each weakness
    weakness_to_types_count = {}
    for row in data:
        weakness = row['weakness']
        pokemon_type = row['type']
        if weakness not in weakness_to_types_count:
            weakness_to_types_count[weakness] = Counter()
        weakness_to_types_count[weakness][pokemon_type] += 1

    # Fill in missing type values based on the most common type for each weakness
    for row in data:
        if row['type'] == 'NaN':
            weakness = row['weakness']
            most_common_type = None
            if weakness in weakness_to_types_count:
                types_count = weakness_to_types_count[weakness]
                most_common_type = max(types_count.items(), key=lambda x: (x[1], x[0]))[0]
            else:
                most_common_type = "normal"
            row['type'] = weakness_to_type_mapping.get(weakness, most_common_type)

    #Updated data goes to the new CSV file
    with open("pokemonResults.csv", mode='w', newline='') as file:
        fieldnames = csv_reader.fieldnames
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(data)

def method_3():

    return None


            
def main():
    #a1 = method_1('pokemonTrain.csv')
    #print(a1)
    a2 = method_2('pokemonTrain.csv')
    a3 = method_3('pokemonTrain.csv')
main()  
