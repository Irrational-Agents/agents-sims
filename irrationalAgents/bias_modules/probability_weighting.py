def compute_weight(prob, gamma):
    """
    Tversky & Kahneman  w(p) = p^gamma / (p^gamma + (1-p)^gamma)^(1/gamma)
    """
    denominator = (prob ** gamma + (1 - prob) ** gamma) ** (1 / gamma)
    return (prob ** gamma) / denominator