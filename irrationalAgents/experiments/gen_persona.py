
from itertools import product
import csv
import numpy as np
import random

def get_emotion_base_weights(traits_dict):

    # 这里假设每个情绪都与人格特征有关
    weights = {
        'anger': 0.1,
        'disgust': 0.1,
        'fear': 0.1,
        'happiness': 0.2,
        'sadness': 0.1,
        'surprise': 0.2,
        'neutral': 0.2
    }
    
    # Neuroticism effects
    if traits_dict['Neuroticism'] == 'high':
        weights['fear'] += 0.2
        weights['sadness'] += 0.2
        weights['anger'] += 0.1
        weights['happiness'] -= 0.2
        weights['neutral'] -= 0.1
    elif traits_dict['Neuroticism'] == 'low':
        weights['happiness'] += 0.1
        weights['neutral'] += 0.1
        weights['fear'] -= 0.1
        weights['sadness'] -= 0.1
    
    # Extraversion effects
    if traits_dict['Extraversion'] == 'high':
        weights['happiness'] += 0.2
        weights['surprise'] += 0.1
        weights['neutral'] -= 0.1
        weights['fear'] -= 0.1
    elif traits_dict['Extraversion'] == 'low':
        weights['neutral'] += 0.2
        weights['happiness'] -= 0.1
        weights['surprise'] -= 0.1
    
    # Agreeableness effects
    if traits_dict['Agreeableness'] == 'high':
        weights['anger'] -= 0.1
        weights['disgust'] -= 0.1
        weights['happiness'] += 0.1
        weights['neutral'] += 0.1
    elif traits_dict['Agreeableness'] == 'low':
        weights['anger'] += 0.2
        weights['disgust'] += 0.1
        weights['happiness'] -= 0.1
    
    # Conscientiousness effects
    if traits_dict['Conscientiousness'] == 'high':
        weights['neutral'] += 0.1
        weights['happiness'] += 0.1
        weights['surprise'] -= 0.1
    elif traits_dict['Conscientiousness'] == 'low':
        weights['surprise'] += 0.1
        weights['neutral'] -= 0.1
    
    # Openness effects
    if traits_dict['Openness'] == 'high':
        weights['surprise'] += 0.1
        weights['neutral'] -= 0.1
    elif traits_dict['Openness'] == 'low':
        weights['neutral'] += 0.1
        weights['surprise'] -= 0.1

    weights = {k: max(0.01, v) for k, v in weights.items()}
    
    # Normalize
    total = sum(weights.values())
    weights = {k: v/total for k, v in weights.items()}
    
    return weights


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
    for name, combo in zip(generate_unique_names(len(combinations)), combinations):
        personality_dict = {'Name': name}
        
        for trait, value in zip(traits, combo):
            personality_dict[trait] = value
        
        emotion_weights = get_emotion_base_weights(personality_dict)
        
        for emotion in emotions:
            personality_dict[emotion] = round(emotion_weights[emotion], 3)
        result.append(personality_dict)

    filename = 'personas.csv'
    fieldnames = ['Name'] + traits + emotions

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(result)

        return result



if __name__ == "__main__":
    generate_personas()

    
    
