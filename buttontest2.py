import pygame

# Pygame initialisieren
pygame.init()
screen = pygame.display.set_mode((400, 300))

# Button erstellen
button_surface = pygame.Surface((150, 50))
button_surface.fill((0, 128, 255))  # Füllt den Button mit Blau

# Schrift hinzufügen
font = pygame.font.Font(None, 36)
text = font.render("Click Me", True, (255, 255, 255))
button_surface.blit(text, (25, 10))  # Text auf den Button zeichnen

# Hauptschleife
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Button zeichnen
    screen.fill((0, 0, 0))  # Hintergrund schwarz
    screen.blit(button_surface, (0, 0))  # Button in die Mitte setzen
    pygame.display.flip()  # Aktualisiert den Bildschirm

pygame.quit()
