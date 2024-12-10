# Action configuration
AVAILABLE_ACTIONS = ["moving", "interacting", "thinking", "sleeping"]
ACTION_COOLDOWN = 5  # seconds

# Planning configuration
MAX_PLAN_STEPS = 10
PLAN_HORIZON = 24  # hours

# Personality traits
PERSONALITY_DIMENSIONS = ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]
TRAIT_RANGE = (0, 100)

# Emotion configuration
EMOTION_TYPES = ["happy", "sad", "angry", "afraid", "disgusted", "surprised", "neutral"]
EMOTION_INTENSITY_RANGE = (0, 10)

# Growth configuration
GROWTH_RATE = 0.01
MAX_GROWTH_PER_CYCLE = 0.1

# Memory configuration
MEMORY_IMPORTANCE_THRESHOLD = 0.5
MEMORY_DECAY_RATE = 0.99
