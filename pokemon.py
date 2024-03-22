import csv
from collections import Counter
from pathlib import Path


def method_1(f):
    fire_count = 0
    fire_above_level_40_count = 0

    with open(f, mode='r', newline='') as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            #Check if the Pokémon is of type "fire"
            if row['type'] == 'fire':
                fire_count += 1
                # Check if the Pokémon's level is at or above 40
                if row['level'] and float(row['level']) >= 40:
                    fire_above_level_40_count += 1

    #Calculate the percentage
    if fire_count > 0:
        percentage = (fire_above_level_40_count / fire_count) * 100
    else:
        percentage = 0

    #Round off the percentage
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

    #Count occurrences of types for each weakness
    weakness_to_types_count = {}
    for row in data:
        weakness = row['weakness']
        pokemon_type = row['type']
        if weakness not in weakness_to_types_count:
            weakness_to_types_count[weakness] = Counter()
        weakness_to_types_count[weakness][pokemon_type] += 1

    #Fill in missing type values based on the most common weakness
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

    #Updated data goes into new file
    with open("pokemonResults.csv", mode='w', newline='') as file:
        fieldnames = csv_reader.fieldnames
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(data)

def method_3(f):
    threshold_level = 40

    #Lists to store the attack, defense, and hit points for pokemons with levels above 40
    atk_above_threshold = []
    def_above_threshold = []
    hp_above_threshold = []
    atk_below_threshold = []
    def_below_threshold = []
    hp_below_threshold = []

    with open(f, mode='r', newline='') as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            level = float(row['level'])
            atk = row['atk']
            def_ = row['def']
            hp = row['hp']
            
            #Check if atk, def, and hp are empty
            if atk != 'NaN':
                atk = float(atk)
            else:
                atk = None
            
            if def_ != 'NaN':
                def_ = float(def_)
            else:
                def_ = None
            
            if hp != 'NaN':
                hp = float(hp)
            else:
                hp = None
            
            #Fill the lists based on the level
            if level > threshold_level:
                if atk is not None:
                    atk_above_threshold.append(atk)
                if def_ is not None:
                    def_above_threshold.append(def_)
                if hp is not None:
                    hp_above_threshold.append(hp)
            else:
                if atk is not None:
                    atk_below_threshold.append(atk)
                if def_ is not None:
                    def_below_threshold.append(def_)
                if hp is not None:
                    hp_below_threshold.append(hp)

    #Calculate the average values 
    avg_atk_above_threshold = round(sum(atk_above_threshold) / len(atk_above_threshold), 1) if atk_above_threshold else None
    avg_def_above_threshold = round(sum(def_above_threshold) / len(def_above_threshold), 1) if def_above_threshold else None
    avg_hp_above_threshold = round(sum(hp_above_threshold) / len(hp_above_threshold), 1) if hp_above_threshold else None
    avg_atk_below_threshold = round(sum(atk_below_threshold) / len(atk_below_threshold), 1) if atk_below_threshold else None
    avg_def_below_threshold = round(sum(def_below_threshold) / len(def_below_threshold), 1) if def_below_threshold else None
    avg_hp_below_threshold = round(sum(hp_below_threshold) / len(hp_below_threshold), 1) if hp_below_threshold else None

    #Fill in missing values based on the calculated averages
    with open(f, mode='r', newline='') as file:
        csv_reader = csv.DictReader(file)
        data = list(csv_reader)

    for row in data:
        level = float(row['level'])
        if level > threshold_level:
            if row['atk'] == 'NaN':
                row['atk'] = avg_atk_above_threshold
            if row['def'] == 'NaN':
                row['def'] = avg_def_above_threshold
            if row['hp'] == 'NaN':
                row['hp'] = avg_hp_above_threshold
        else:
            if row['atk'] == 'NaN':
                row['atk'] = avg_atk_below_threshold
            if row['def'] == 'NaN':
                row['def'] = avg_def_below_threshold
            if row['hp'] == 'NaN':
                row['hp'] = avg_hp_below_threshold

    #Updated file goes into CSV
    with open(f, mode='w', newline='') as file:
        fieldnames = csv_reader.fieldnames
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(data)



def method_4(f):
    #Dictionary to store Pokémon types and their associated personalities
    type_to_personality_mapping = {}

    with open(f, mode='r', newline='') as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            pokemon_type = row['type']
            personality = row['personality']
            
            #Skip rows with missing type or personality
            if pokemon_type != 'NaN' and personality != 'NaN':
                # If the type already exists in the dictionary, append
                if pokemon_type in type_to_personality_mapping:
                    type_to_personality_mapping[pokemon_type].append(personality)
                else:
                    #If the type is new, create a new list
                    type_to_personality_mapping[pokemon_type] = [personality]

    #Sort the types alphabetically
    sorted_types = sorted(type_to_personality_mapping.keys())
    for pokemon_type in sorted_types:
        type_to_personality_mapping[pokemon_type].sort()

    #Write the dictionary to a file
    with open('pokemon4.txt', mode='w') as output_file:
        output_file.write("Pokemon type to personality mapping:\n")
        for pokemon_type in sorted_types:
            personalities = ", ".join(type_to_personality_mapping[pokemon_type])
            output_file.write(f"  {pokemon_type}: {personalities}\n")

def method_5(f):
    target_stage = 3.0

    #List to store Hit Points of Pokémon with stage 3.0
    hp_values = []

    with open(f, mode='r', newline='') as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            stage = float(row['stage'])
            hp = row['hp']
            
            #Skip rows with missing hp or stage, or with stage other than 3.0
            if hp != 'NaN' and stage == target_stage:
                hp_values.append(float(hp))

    #Calculate the average Hit Points for Pokémon with stage 3.0
    if hp_values:
        average_hp = sum(hp_values) / len(hp_values)
    else:
        average_hp = 0

    average_hp = round(average_hp)

    # Write the average value to a file
    with open('pokemon5.txt', mode='w') as output_file:
        output_file.write(f"Average hit point for Pokemons of stage {target_stage} = {average_hp}\n")

            
def main():
    #a1 = method_1('pokemonTrain.csv')
    #print(a1)
   # a2 = method_2('pokemonTrain.csv')
    #a3 = method_3('pokemonTrain.csv')
    #a4 = method_4("pokemonTrain.csv")
    a5 = method_5("pokemonTrain.csv")
main()  
