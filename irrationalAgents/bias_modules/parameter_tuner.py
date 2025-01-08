def determine_parameters(emotion, personality):
    """
    感情(emotion)、性格(personality)情報を元に
    α, β, γ, λ を動的に決定する。
    """
    # Default parameters
    alpha, beta, gamma, lambda_ = 0.8, 0.8, 0.9, 1.5

    # Adjust parameters based on emotion
    if emotion == "anger":
        alpha, beta, gamma, lambda_ = 0.9, 0.7, 0.7, 1.2
    elif emotion == "disgust":
        alpha, beta, gamma, lambda_ = 0.8, 0.6, 0.9, 2.0
    elif emotion == "fear":
        alpha, beta, gamma, lambda_ = 0.7, 0.5, 0.8, 1.8
    elif emotion == "happiness":
        alpha, beta, gamma, lambda_ = 1.0, 0.9, 1.0, 1.0
    elif emotion == "sadness":
        alpha, beta, gamma, lambda_ = 0.7, 0.6, 0.8, 1.5
    elif emotion == "surprise":
        alpha, beta, gamma, lambda_ = 0.8, 0.7, 0.6, 1.3
    elif emotion == "neutral":
        alpha, beta, gamma, lambda_ = 0.8, 0.8, 0.9, 1.5

    # Big Five
    personality_influence = {
        "Openness": {"high": 0.1, "neutral": 0.0, "low": -0.1},
        "Conscientiousness": {"high": 0.0, "neutral": 0.0, "low": 0.0},
        "Extraversion": {"high": 0.1, "neutral": 0.0, "low": -0.1},
        "Agreeableness": {"high": 0.0, "neutral": 0.0, "low": 0.0},
        "Neuroticism": {"high": -0.1, "neutral": 0.0, "low": 0.1},
    }

    for trait, level in personality.items():
        if trait == "Openness":
            alpha += personality_influence[trait][level]
            gamma += personality_influence[trait][level]
        elif trait == "Conscientiousness":
            beta += personality_influence[trait][level]
            lambda_ += personality_influence[trait][level]
        elif trait == "Extraversion":
            alpha += personality_influence[trait][level]
            gamma += personality_influence[trait][level]
            if level == "high":
                lambda_ -= 0.1
            elif level == "low":
                lambda_ += 0.1
        elif trait == "Agreeableness":
            beta += personality_influence[trait][level]
            lambda_ += personality_influence[trait][level]
        elif trait == "Neuroticism":
            alpha += personality_influence[trait][level]
            beta += personality_influence[trait][level]
            if level == "high":
                lambda_ += 0.2
            elif level == "low":
                lambda_ -= 0.2

    return alpha, beta, gamma, lambda_