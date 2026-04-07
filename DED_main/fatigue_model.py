def calculate_exhaustion(screen_time, typing, mouse):
    """
    screen_time : minutes
    typing      : key presses
    mouse       : mouse clicks
    """
    score = (
        screen_time * 1.0 +
        typing * 0.01 +
        mouse * 0.01
    )
    return round(score, 2)
