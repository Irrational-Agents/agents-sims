def compute_value(outcome, alpha, beta, lambda_):
    """
    outcome >= 0 : x^alpha
    outcome < 0 : -lambda * ((-x)^beta)
    """
    if outcome >= 0:
        return outcome ** alpha
    else:
        return -lambda_ * ((-outcome) ** beta)