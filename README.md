# Artistic installation project "Chandelier
![Chandelier installation]
(https://github.com/MartwyJez/Chandelier/blob/master/chandelier_installation_movie.WEBP)
## Main idea
We wanted to create interactive sequence about schizophrenia related topics.
#### It is made made from:
- Raspberry Pi 3 Model A+
- 4 pin RGB LED strip
- 2 MOSFET transistors
- 3 movement sensors
- jack connected, earphone-shaped speaker
- bluetooth speaker
- bluetooth remote button

#### Main steps of sequence are:
1. White, pulsing light, ambient sounds from bt speaker - waiting for movement
2. Movement - telephone ring bell from bt speaker, red light, waiting for button push
3. After button push - psychodelic voice from jack speaker, red pulsing light, waiting for another button push
4. If push last:

   - \> 3 sec - You lose, information about schizophrenia from bt speaker, red light

   - < 3 sec - You win, information about schizophrenia from bt speaker, white light
5. Break between sequences, ambient sounds from bt speaker, white pulsing lights
6. Repeat


## Main problems:
1. Not commented, messy code. It was written by one person in quite limited amount of time. But it recoverable messy in case that we will continue our project.
2. Bluetooth button - one hell ride with it - this technology it's not meant to be used on "wait long for input" mode. Remote is get constantly disconnected. This is main of reason why main program is looks like it looks.
In next iteration we surely switch for cable-connected button and maybe speaker too.
3. Movement sensors are too sensitive, we couldn't placed it in way that no sensor won't instantly sense a movement. Because of that we decided to add hardcoded pause between waiting for movement and continuing. On top of that I had to change mode of detecting - reacting to change from 0 (not detecting) to 1 (detecting) was replaced by just checking if even one sensor send 1.
4. It was my playground for learning how to write someting asynchronized and multi-threaded.
5. Using VLC python library - as much as it was the simplest sound player that I could find, later I would rather switch to something lighter.
## Main features
1. Search, trust, pair, disconnect after error (with possibilty of retries) with bluetooth device using bluetoothctl. **After all it wasn't best choice to write this in python, it's look very messy. Bash scripts would fit much more.** Unfortunatelly I didn't find any python library to get that much easy control of bluetooth like from bluetoothctl.
2. Get pulse-audio sink from bluetooth speaker to later use it.
3. Asynchronized waiting for bt button push.
4. Managing pulse-audio sinks, possibility to create combined one.
5. Control rgb led light using MOSFET transistor. We had only two because we wanted either only red or white light.
6. Asynchronized waiting for movment detection.

## Usage
1. Install VLC
2. `pip install -r requirments.txt`
3. From main directory: `pip install .`
4. `python[3] -m chandelier`
