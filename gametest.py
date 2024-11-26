import sys
import pygame as pg
import numpy as np

# Mandelbrot-Funktion mit NumPy-Vektorisierung
def brot_set(xmin, xmax, ymin, ymax, width, height, max_iter):
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)
    X, Y = np.meshgrid(x, y)
    C = X + 1j * Y  # Erstelle das komplexe Array

    Z = np.zeros(C.shape, dtype=complex)
    iterations = np.zeros(C.shape, dtype=int)

    # Iterationen für jedes Pixel
    for i in range(max_iter):
        mask = np.abs(Z) <= 2  # Nur Punkte, die noch im Bereich sind
        Z[mask] = Z[mask] ** 2 + C[mask]
        iterations[mask] += mask[mask]  # Iteration erhöhen

    return iterations

# Farbschemata (aus Chat-GPT generiert)
def grayscale(iteration, max_iter):
    t = iteration / max_iter
    gray = int(255 * t)
    return (gray, gray, gray)

def blue_white(iteration, max_iter):
    t = iteration / max_iter
    return (0, 0, int(255 * t))

def rainbow(iteration, max_iter):
    t = iteration / max_iter
    r = int(255 * t)
    g = int(255 * (1 - t))
    b = int(255 * (0.5 + 0.5 * t))
    return (r, g, b)

def green_purple(iteration, max_iter):
    t = iteration / max_iter
    r = int(255 * (1 - t))
    g = int(255 * t)
    b = int(255 * (t * 0.5))
    return (r, g, b)

def bright(iteration, max_iter):
    t = iteration / max_iter
    r = int(255 * t)
    g = int(255 * (0.8 * t))
    b = int(255 * (0.6 * t))
    return (r, g, b)

# Farbdefinitionen basierend auf Positionen (Wikipedia-Style)
color_points = [
    (0.0, (0, 7, 100)),
    (0.16, (32, 107, 203)),
    (0.42, (237, 255, 255)),
    (0.6425, (255, 170, 0)),
    (0.8575, (0, 2, 0))
]

def interpolate_color(position):
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
    t = iteration / max_iter
    return interpolate_color(t)

# Reihenfolge Farbschemata
color_schemes = [custom_color_scheme, grayscale, blue_white, rainbow, green_purple, bright]

def main():
    # Parameter für die Mandelbrotmenge
    xmin, xmax, ymin, ymax = -2.0, 1.0, -1.5, 1.5
    width, height = 400, 400  # Auflösung
    max_iter = 100

    # Initialisieren pygame
    pg.init()
    screen = pg.display.set_mode((width, height))
    pg.display.set_caption("Matzes Mandelbrot-Generator")
    clock = pg.time.Clock()

    # Mandelbrotmenge berechnen
    mandelbrot_set = brot_set(xmin, xmax, ymin, ymax, width, height, max_iter)

    # Erstelle eine Surface für das Mandelbrot-Bild
    mandelbrot_surface = pg.Surface((width, height))
    
    # Start mit dem ersten Farbschema
    current_color_scheme = 0  
    
    # Zoom
    dragging = False
    start_pos = None
    end_pos = None

    # Hauptschleife
    running = True
    while running:
        # Steuerung
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RIGHT:  # Nächstes Farbschema
                    current_color_scheme = (current_color_scheme + 1) % len(color_schemes)
                elif event.key == pg.K_LEFT:  # Vorheriges Farbschema
                    current_color_scheme = (current_color_scheme - 1) % len(color_schemes)
                elif pg.K_1 <= event.key <= pg.K_9:  # Direktwahl der Farbschemata 1-9
                    current_color_scheme = (event.key - pg.K_1) % len(color_schemes)
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:  # Linke Maustaste
                    dragging = True
                    start_pos = pg.mouse.get_pos() # Nimm Position beim drücken
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1 and dragging:
                    dragging = False
                    end_pos = pg.mouse.get_pos() # Nimm Position beim loslassen

                    # Box-Koordinaten sortieren
                    x1, y1 = start_pos
                    x2, y2 = end_pos

                    # Berechne die Breite und Höhe der Box
                    size = min(abs(x2 - x1), abs(y2 - y1))

                    # Mache die Box quadratisch
                    if x2 < x1:
                        x_min_pix = x1 - size
                        x_max_pix = x1
                    else:
                        x_min_pix = x1
                        x_max_pix = x1 + size
                    
                    if y2 < y1:
                        y_min_pix = y1 - size
                        y_max_pix = y1
                    else:
                        y_min_pix = y1
                        y_max_pix = y1 + size

                    # Pixel in komplexe Koordinaten umrechnen
                    new_xmin = xmin + (x_min_pix / width) * (xmax - xmin)
                    new_xmax = xmin + (x_max_pix / width) * (xmax - xmin)
                    new_ymin = ymin + (y_min_pix / height) * (ymax - ymin)
                    new_ymax = ymin + (y_max_pix / height) * (ymax - ymin)

                    # Neue Werte setzen
                    xmin, xmax, ymin, ymax = new_xmin, new_xmax, new_ymin, new_ymax

                    # Mandelbrotmenge neu berechnen
                    mandelbrot_set = brot_set(xmin, xmax, ymin, ymax, width, height, max_iter)

        # Aktualisiere die Mandelbrot-Surface
        get_color = color_schemes[current_color_scheme]
        for y in range(height):
            for x in range(width):
                iteration = mandelbrot_set[y, x]
                color = get_color(iteration, max_iter)
                mandelbrot_surface.set_at((x, y), color)

        # Zeichne das Mandelbrot-Bild auf den Bildschirm
        screen.blit(mandelbrot_surface, (0, 0))
        
        # FPS-Wert abrufen und anzeigen
        fps = clock.get_fps()  # Abrufen der aktuellen FPS
        font = pg.font.SysFont("Arial", 20)
        fps_text = font.render(f"FPS: {fps:.2f}", True, (255, 255, 255))
        screen.blit(fps_text, (10, 10))  # FPS oben links anzeigen

        # Box zeichnen, falls Dragging aktiv ist
        if dragging and start_pos:
            current_pos = pg.mouse.get_pos()
            size = min(abs(current_pos[0] - start_pos[0]), abs(current_pos[1] - start_pos[1]))
            x_min = min(current_pos[0], start_pos[0])
            y_min = min(current_pos[1], start_pos[1])

            # Zeichne das quadratische Rechteck
            pg.draw.rect(
                screen,
                (255, 255, 255),
                pg.Rect(x_min, y_min, size, size),
                1
            )
            
        # FPS begrenzen
        clock.tick(60)
        # Bildschirm aktualisieren
        pg.display.flip()

    pg.quit()

# Programm starten
if __name__ == "__main__":
    main()
