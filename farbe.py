import numpy as np

# Farbdefinitionen basierend auf Positionen
color_points = [
    (0.0, (0, 7, 100)),
    (0.16, (32, 107, 203)),
    (0.42, (237, 255, 255)),
    (0.6425, (255, 170, 0)),
    (0.8575, (0, 2, 0))
]

def interpolate_color(position):
    """
    Interpoliert die Farbe basierend auf der Position im Farbschema.
    :param position: Float zwischen 0 und 1
    :return: Interpolierte Farbe (R, G, B) als Tuple
    """
    for i in range(len(color_points) - 1):
        pos1, col1 = color_points[i]
        pos2, col2 = color_points[i + 1]
        if pos1 <= position <= pos2:
            # Interpolation zwischen den beiden Punkten
            t = (position - pos1) / (pos2 - pos1)
            r = int(col1[0] + t * (col2[0] - col1[0]))
            g = int(col1[1] + t * (col2[1] - col1[1]))
            b = int(col1[2] + t * (col2[2] - col1[2]))
            return (r, g, b)
    # Rückgabe der letzten Farbe, falls Position > max Position
    return color_points[-1][1]

def custom_color_scheme(iteration, max_iter):
    """
    Erzeugt eine Farbe basierend auf Iteration und dem angegebenen Farbschema.
    :param iteration: Iterationswert
    :param max_iter: Maximale Iterationsanzahl
    :return: Interpolierte Farbe (R, G, B) als Tuple
    """
    t = iteration / max_iter
    return interpolate_color(t)
