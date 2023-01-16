#### To install the needed libraries, I used the following commands:
- ```pip install -U selenium```
- ```pip install numpy```
- ```pip install opencv-python```
- ```pip install pyautogui```
- ```sudo apt install python3-pyaudio```

#### The system that the script was developed and tested on is Ubuntu 20.04 LTS.

#### The flow of the script is as follows:
- the internet connection is tested and if it fails, the script stops.
- a chrome tab opens up on the YouTube home page and presses the accept cookies.
button, which allways pops up (if it fails to do so, the script stops)
- it randomly selects a video/short from the homepage and clicks on it. If the
selected item is a video, then it will proceed to skip the ad if it encounters
a skippable one, otherwise it will play through. If there is an error while
trying to press the play button on the video/short, the script will catch it and
will stop the execution.
- then it starts the recording of both screen and audio, checking if there is
enough diskspace on the system to perform the writing (if not, the exception
will be caught and the script will terminate).
- after the recording is finished, the ```.wav``` file will be analyzed and the
ouput will be written to a file.
