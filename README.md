# Line Intensity Mapping Animations
Illustrative animations designed to inform of contamination by interlopers at different redshifts. Feel free to use the animations as much as you want [ just please cite/reference me :) also (not required) but would love to see if your slides if you decide to use them!]

The animations are made using `manim`, and so you will need to have that installed before you can run the animations yourself. You can find a guide on installing it [here](https://docs.manim.community/en/stable/installation.html).

## To Execute / Edit for your own needs
#### _First Option: Jupyter_
  - This is if you want to keep everything contained (writing code, seeing your animations, etc.) all in the same place. All 4 animations are within their own cells in the notebook. Run the first cell (functions) and then run whichever animation you want to produce. I do my testing using notebooks

#### _Second Option: Command Line_
  - Running individual animations can be done using `python -m manim -qh pythonfile.py className`. So for for the combined scene it would look like `python -m manim -qh ConeANDLOSAnimation.py combScene`
  - I will say you might have a different form of running it above, if it doesn't work check out the manim documentation (community version). I use a virtual environment for my manim, that may be slightly different than yours too.

The output video will be in subfolder than manim makes. It will make 'partial_movie_files' and also the full mp4 file. 
