# Desktop Pet
This is a python project that makes an interactable desktop pet with animations. Pets are customizable, can have arbitrary amounts of animations, and can easily be added. When run, the pets will cycle animations, move around the sreen by themselve, or be moved by the user's mouse.


## Adding a New Pet
To add a new pet one must:
1. Add a new pet in the pets element in the `config.xml`
2. Add either `.gif` or `.png` files to the `src/sprites/{pet_name}` folder for each animation
3. Define the different animation states the new pet has in `src/animations.py` as a new function and add it to `src.animations.get_animations`. Look at the examples of  `src.animations.get_cat_animations` and `src.animations.get_horse_animations` functions for help.
4. Update the defualt pet in the `config.xml`to the pet you just made

After those 4 steps simply run the project and you should see your pet on your desktop!

## Installation and Testing
`python3 -m venv venv`
`.\venv\Scripts\activate.ps1`
`pip install -r requirements.txt`
`python run.py`

## Bundling and Creating an Executable
We are using [pyinstaller](https://www.pyinstaller.org/) to create and bundle the stand alone executable. To create a new executable after changing files simply call `pyinstaller run.spec` while in the venv and the project's root directory. The bundled executable will be in the  `\dist\DesktopPet` folder. 

File Not Found Exception? Data files, non-python dependencies such as images, must be added explicitly in the `run.spec` file. So, if you added such a file that is not in `src/sprites` you must add it to the `datas` array in `run.spec`.