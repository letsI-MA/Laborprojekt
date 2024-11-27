# This is a Mandelbrot Set Explorer

The idea was to display the __Mandelbrot Set__ in a somewhat appealing manner.
***This project is for me to learn and adapt to problems in software development.***
I did extensive amounts of comments in Version 1 so I can learn and keep the information close by.
At the bottom of this readme I will provide my sources.

### What is a Mandelbrot Set?

The Mandelbrot set is a collection of complex numbers ***c*** for which the sequence generated by the formula:

![formel](https://github.com/user-attachments/assets/c48461e7-eed7-414c-975a-e434a08384fe) 

remains bounded as ***n→∞***.

- Start with ***z<sub>0</sub>*** = ***0***
- Add the constant ***c*** to the square of the current value of ***z***
- Repeat the process to see whether the value of ***z*** stays small _(bounded)_ or grows without limit _(diverges)_

### Visualizing the Mandelbrot Set

- Define a grid of points in the complex plane (real and imaginary numbers)
- For each point ***c***, iterate the formula up to a maximum number of steps
- Check if the magnitude ***z<sub>n</sub>*** remains ***≤2***. If so, c is part of the Mandelbrot set

The first Version is brot.py was just a PoC on matplotlib:
https://github.com/letsI-MA/Laborprojekt/blob/main/brot.py

![brot1](https://github.com/user-attachments/assets/dcd5d943-daa5-4f83-973e-ec6f35a34e25)

In Version 2 I implemented the code into pygame and added these features:

- multiple color schemes, including the style wikipedia uses
- able to switch color schemes on button presses 1-6
- Zoom feature by dragging a square box over the set

![brot2](https://github.com/user-attachments/assets/cfeecf94-5f0f-4583-baf4-3736d35f6e44)


With the help of ChatGPT I've switched from an array-based storage for the elements of the Mandelbrot-Function to vectors which enhanced
the average FPS from 1.2 to 3.5 in 500x500 resolution 🙌.

## Controls

- Numberkeys 1-6 switches between colorschemes
- ESC closes the window and kills the process
- Left-Mouse-Button to draw a square in which to zoom in
- FPS counter in the top left corner

## Sources

### NumPy
[NumPy Documentation](https://numpy.org/doc/2.0/)

### Pygame

- [Pygame Documentation](https://www.pygame.org/docs/)
- [The ultimate introduction to Pygame" - Clear Code](https://www.youtube.com/watch?v=AY9MnQ4x3zk)
  
### Bill's Chaos

- ["Mandelbrot Set, with zoom, python, pygame, numpy, numba" - Bill's Chaos](https://www.youtube.com/watch?v=lrfVTlCx7GY)
- [Bill Chaos' GitHub Project](https://github.com/wburris/Sandbox/blob/master/python/Mandlebrot.py)

### Wikipedia and other links
- ["Mandelbrot-Menge" - Wikipedia](https://de.wikipedia.org/wiki/Mandelbrot-Menge)