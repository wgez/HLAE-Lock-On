# HLAE Lock On Tool
A simple desktop app that builds a campath where a stationary camera will automatically turn to face your player model.

# Installation
1. Download the latest release: https://github.com/wgez/HLAE-Lock-On/releases/latest
2. Extract and run executable "HLAE LockOn Tool".

# How to Use
1. Spam campath points while you're in firstperson.
2. Save the resulting campath file.
3. Move to the position you'd like your camera to be stationary (where the cam will rotate to face your player model).
4. Use the command "mirv_input position" and copy your position coordinates.
5. Open the HLAE LockOn Tool.
6. Paste your position coordinates in field 1, select your campath file in field 2.
7. Run the program, select your output campath filename, and it will auto-generate the campath file.
8. Load the newly generated campath file through HLAE and wonder why we gotta go through all this work for this feature.

# Issues
1. The generated campath file is still susceptible to demo file lag. Your campath could stutter/jitter a bit if the demo lags (you can try to remove some jitter through video editing).
2. You can only do this reliably on your own player model. If you want to try this on a different player, you'll have to do your best to manually track their position with campath points (pause and draw!). If anything, you may be better off just manually drawing a rotating campath that tracks your desired player.

# How to Build (for developers)
1. Install GIT bash (to obtain source code) - https://git-scm.com/downloads
2. Install your favorite IDE (eg. Visual Studio Code) - https://code.visualstudio.com/
3. Install Python - https://www.python.org/downloads/
4. Obtain the source code from https://github.com/wgez/HLAE-Lock-On into a folder you like (git clone).
5. In VSCode, open a terminal and go to the HLAE-Lock-On directory (cd).
6. Install PyInstaller by entering in the terminal: pip install pyinstaller
7. Build the executable by entering in the terminal: pyinstaller --onefile --windowed hlae_lockon_gui.py
8. The executable will found in the newly created dist/ folder.
Note: I assumed these are the steps. I can add a more robust version if issues are found.