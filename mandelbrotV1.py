# numpy um mit Arrays zu arbeiten
import numpy as np
# matplot um es graphisch darzustellen
import matplotlib.pyplot as plt 

def brot(c, max_iter):                                          # Komplexe Nummer die getestet wird und Anzahl der Iterationen
    z = 0                                                       # Initialisierung von z
    for n in range(max_iter):                                   # Schleife läuft bis max_iter erreicht wird
        if abs(z) > 2:                                          # Wenn der Betrag von z größer als 2 wird => Schleife abbrechen => keine Mandelbrotmenge
            return n                                            # Menge der Iterationen zu zeigen, dass c nicht zur Menge gehört
        z = z * z + c                                           # Wenn z den Iterationen nicht entkommt ist c wahrscheinlich eine Mandelbrotmenge // Mandelbrotformel
    return max_iter                                             # Wenn nicht abgebrochen wird => return max_iter

#

def brot_set(xmin, xmax, ymin, ymax, width, height, max_iter):  # '_'min/max sind die Achsen , width/height die Dimensionen des Graphen in Pixeln, max_iter Iterations-Anzahl
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, width)
    
    mset = np.zeros((height, width))                            # zweidimensionales Array: speichert jedes Element der Berechnung
    
    for i in range (height):                                    # Schleife für Rows
        for j in range(width):                                  # Schleife für Columns
            c = complex(x[j], y[i])                             # Für jede Position wird eine komplexe Zahl 'c' erzeugt
            mset[i,j] = brot(c, max_iter)                       # Berechnet ob und wie viele Iterationen gebraucht wurden um zu entkommen. Ergebnis wird als mset[] gespeichert
            
    return mset                                                 # Rückgabe des Arrays

#

xmin, xmax, ymin, ymax = -2.0, 1.0, -1.5, 1.5                   # x = Von -2 bis 1 // y = Von -1.5 bis 1.5
width, height = 1000, 1000                                      # Auflösung des Rasters
max_iter = 100                                                  # Anzahl der Iterationen die geprüft werden sollen

#

mandelbrot_image = brot_set(xmin, xmax, ymin, ymax, width, height, max_iter)    # brot_set wird ausgeführt und mandelbrot_image enthält ein zweidimensionales Array mit den Iterationswerten für jeden Punkt im Raster

#

plt.imshow(mandelbrot_image, extent=[xmin, xmax, ymin, ymax], cmap='hot')       # Grafik wird angezeigt. 'extent' legt die Achsenbezeichnung fest. 'hot' ist das Farbscheme (kleine Werte dunkler)
plt.colorbar()                                                                  # Farbenlegende
plt.title('Matzes Brotgenerator')                                               # Titel
plt.xlabel('Re(c)')                                                             # Reale Achse
plt.ylabel('Im(c)')                                                             # Imaginäre Achse
plt.show()                                                                      # Zeigt schlussendlich das Fenster