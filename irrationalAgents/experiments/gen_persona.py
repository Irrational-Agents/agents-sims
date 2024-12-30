from itertools import product
import csv
import numpy as np
import random


def generate_unique_names(n):
    first_names = [
        "Emma", "Liam", "Olivia", "Noah", "Ava", "Oliver", "Isabella", "William", "Sophia", "James",
        "Yuki", "Kai", "Mei", "Hiroshi", "Sakura", "Chen", "Wei", "Ming", "Jin", "Hui",
        "Sofia", "Lucas", "Maria", "Diego", "Ana", "Carlos", "Elena", "Miguel", "Laura", "Pablo",
        "Mohammed", "Aisha", "Omar", "Fatima", "Ahmad", "Zara", "Hassan", "Leila", "Ali", "Noor",
        "Alexander", "Anna", "Ivan", "Natasha", "Dmitri", "Ekaterina", "Viktor", "Olga", "Sergei", "Nina",
        "David", "Sarah", "Michael", "Emily", "Daniel", "Sophie", "Matthew", "Alice", "Joseph", "Grace",
        "Marcus", "Luna", "Leo", "Aurora", "Felix", "Clara", "Max", "Julia", "Thomas", "Eva"
    ]
    
    last_names = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
        "Tanaka", "Yamamoto", "Kim", "Lee", "Wang", "Zhang", "Liu", "Chen", "Yang", "Huang",
        "Gonzalez", "Lopez", "Perez", "Sanchez", "Ramirez", "Torres", "Flores", "Rivera", "Gomez", "Diaz",
        "Al-Sayed", "Khan", "Patel", "Kumar", "Singh", "Shah", "Malik", "Ahmed", "Hassan", "Ali",
        "Ivanov", "Petrov", "Smirnov", "Kuznetsov", "Popov", "Sokolov", "Lebedev", "Kozlov", "Novikov", "Morozov",
        "Anderson", "Taylor", "Wilson", "Martin", "Thompson", "White", "Roberts", "Lewis", "Clark", "Young"
    ]
    
    names = []
    used_combinations = set()
    
    while len(names) < n:
        first = random.choice(first_names)
        last = random.choice(last_names)
        full_name = f"{first} {last}"
        
        if full_name not in used_combinations:
            names.append(full_name)
            used_combinations.add(full_name)
            
    return names


def generate_personas():
    traits = ['Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Neuroticism']
    values = ['low', 'medium', 'high']
    emotions = ['anger', 'disgust', 'fear', 'happiness', 'sadness', 'surprise', 'neutral']

    combinations = list(product(values, repeat=len(traits)))

    result = []
    for emotion in emotions:
        for name, combo in zip(generate_unique_names(len(combinations)), combinations):
            personality_dict = {'Name': name}
            personality_dict['Dominance_emotion'] = emotion
            
            for trait, value in zip(traits, combo):
                personality_dict[trait] = value
            
            result.append(personality_dict)
    
    random.shuffle(result)

    filename = 'personas.csv'
    fieldnames = ['Name'] + traits + ['Dominance_emotion']

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(result)

        return result



if __name__ == "__main__":
    generate_personas()

    
    
