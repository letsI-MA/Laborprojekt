import sys
import pygame as pg
import numpy as np

# Mandelbrot-Funktion Vektoren
def brot_set(xmin, xmax, ymin, ymax, width, height, max_iter):
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)
    X, Y = np.meshgrid(x, y)
    C = X + 1j * Y  # Erstelle das komplexe Array

    Z = np.zeros_like(C)
    iterations = np.zeros(C.shape, dtype=int)
    
    # Maske für non-divergend Punkte
    mask = np.ones(C.shape, dtype=bool)

    for i in range(max_iter):
        Z[mask] = Z[mask]** 2 + C[mask]  # Update nur non-diverged Punkte
        mask = (np.abs(Z) <= 2)  # Update Maske für gebundene Punkte
        iterations[mask] = i  # Update Zähler

    return iterations

# Farbschemata (aus Chat-GPT generiert)
def graustufen(iteration, max_iter):
    t = iteration / max_iter
    gray = (255 * t).astype(int)
    return np.dstack([gray, gray, gray])

def blauweiss(iteration, max_iter):
    t = (iteration / max_iter).astype(int)
    return np.dstack([np.zeros_like(t), np.zeros_like(t), 255 * t])

def regenbogen(iteration, max_iter):
    t = iteration / max_iter
    r = (255 * t).astype(int)
    g = (255 * (1 - t)).astype(int)
    b = (255 * (0.5 + 0.5 * t)).astype(int)
    return np.dstack([r, g, b])

def grünlila(iteration, max_iter):
    t = iteration / max_iter
    r = (255 * (1 - t)).astype(int)
    g = (255 * t).astype(int)
    b = (255 * (0.5 * t)).astype(int)
    return np.dstack([r, g, b])

def hell(iteration, max_iter):
    t = iteration / max_iter
    r = (255 * t).astype(int)
    g = (255 * (0.8 * t)).astype(int)
    b = (255 * (0.6 * t)).astype(int)
    return np.dstack([r, g, b])

# Farbdefinitionen basierend auf Positionen (Wikipedia-Style)
color_points = [
    (0.0, (0, 7, 100)),
    (0.16, (32, 107, 203)),
    (0.42, (237, 255, 255)),
    (0.6425, (255, 170, 0)),
    (0.8575, (0, 2, 0))
]

def interpolate_color(iterations, max_iter):
    t = iterations / max_iter
    color = np.zeros((*t.shape, 3), dtype=int)

    for i in range(len(color_points) - 1):
        p1, c1 = color_points[i]
        p2, c2 = color_points[i + 1]
        mask = (p1 <= t) & (t < p2)
        interp = (t[mask] - p1) / (p2 - p1)
        for j in range(3):
            color[..., j][mask] = (c1[j] + interp * (c2[j] - c1[j])).astype(int)

    return color

def custom_color_scheme(iterations, max_iter):
    return interpolate_color(iterations, max_iter)

# Reihenfolge Farbschemata
color_schemes = [custom_color_scheme, graustufen, blauweiss, regenbogen, grünlila, hell]

def main():
    # Parameter für die Mandelbrotmenge
    xmin, xmax, ymin, ymax = -2.0, 1.0, -1.5, 1.5
    width, height = 500, 500    # Auflösung
    max_iter = 500              # Anzahl der Iterationen

    # Initialisieren pygame
    pg.init()
    screen = pg.display.set_mode((width, height))           # Auflösung aus dem Absatz oben
    pg.display.set_caption("Matzes Mandelbrot-Generator")   # Titel
    clock = pg.time.Clock()                                 # Initialisierung der Ticks

    # Mandelbrotmenge berechnen
    mandelbrot_set = brot_set(xmin, xmax, ymin, ymax, width, height, max_iter)
    
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
            # Wenn ESC gedrückt wird => Schließe Simulation
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
                # Farbsteuerung durch Pfeiltasten
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RIGHT:  # Nächstes Farbschema
                    current_color_scheme = (current_color_scheme + 1) % len(color_schemes)
                elif event.key == pg.K_LEFT:  # Vorheriges Farbschema
                    current_color_scheme = (current_color_scheme - 1) % len(color_schemes)
                elif pg.K_1 <= event.key <= pg.K_9:  # Direktwahl der Farbschemata 1-9
                    current_color_scheme = (event.key - pg.K_1) % len(color_schemes)
            # Kasten zum Zoomen
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
        
        # Farbe selektieren
        colors = color_schemes[current_color_scheme](mandelbrot_set, max_iter)
        pg.surfarray.blit_array(screen, np.transpose(colors, (1, 0, 2)))
        
        # FPS-Wert abrufen und anzeigen
        fps = clock.get_fps()   # Abrufen der aktuellen FPS
        font = pg.font.SysFont("Arial", 20) # Schriftart
        fps_text = font.render(f"FPS: {fps:.2f}", True, (255, 0, 0)) # FPS rot
        screen.blit(fps_text, (10, 10))  # FPS oben links anzeigen

        # Box zeichnen, falls Dragging aktiv ist
        if dragging and start_pos:
            current_pos = pg.mouse.get_pos()
            size = min(abs(current_pos[0] - start_pos[0]), abs(current_pos[1] - start_pos[1]))
            x_min = min(current_pos[0], start_pos[0])
            y_min = min(current_pos[1], start_pos[1])

            # Zeichne das quadratische Rechteck
            pg.draw.rect(screen, (255, 0, 0), pg.Rect(x_min, y_min, size, size), 1)
            
        # FPS begrenzen
        clock.tick(60)
        # Bildschirm aktualisieren
        pg.display.flip()

    pg.quit()

# Programm starten
if __name__ == "__main__":
    main()
