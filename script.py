from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import random
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.request
import cv2
import numpy as np
import pyautogui
import wave
import pyaudio
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotInteractableException 
from scipy.io import wavfile
import soundfile as sf
import sys

def is_connected():
    try:
        urllib.request.urlopen('http://google.com')
        return True
    except:
        return False

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# # display screen resolution, get it using pyautogui itself
SCREEN_SIZE = tuple(pyautogui.size())
# # define the codec
fourcc = cv2.VideoWriter_fourcc(*"XVID")
# # frames per second
fps = 12
# # create the video write object
out = cv2.VideoWriter("output.avi", fourcc, 40.0, (SCREEN_SIZE))
# # the time you want to record in seconds
record_seconds = 10

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)



def open_youtube(browser, wait):
    browser.get('http://www.youtube.com')
    browser.maximize_window()

    time.sleep(1)

    # current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("Accessed {} at {}".format(browser.title, current_time))

    # get the accept cookies button and press it to continue
    accept_btn_text = "Accept the use of cookies and other data for the purposes described"

    try:
        wait.until(EC.presence_of_all_elements_located((By.XPATH, "//button[@aria-label='{}']".format(accept_btn_text))))
        acc_cookies_btn = browser.find_elements(By.XPATH, "//button[@aria-label='{}']".format(accept_btn_text))
    except TimeoutException:
        return

    if len(acc_cookies_btn) == 0:
        print("Error! Did not found the accept cookies button")
        browser.quit()
        raise SystemExit
    else:
        acc_cookies_btn = acc_cookies_btn[0]


    browser.execute_script("arguments[0].click()", acc_cookies_btn)
    print("Accepted cookies at {}".format(get_current_time()))

def play_video(browser, wait):
    # get all the videos by thumbnail and access a random one
    wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "yt-image")))
    videos = browser.find_elements(By.TAG_NAME, "yt-image")

    if len(videos) != 0:
        idx = random.randint(0, len(videos) - 1) 

        try:
            browser.execute_script("arguments[0].click()", videos[idx])
        except StaleElementReferenceException:
            wait.until(EC.element_to_be_clickable(videos[idx]))
            videos[idx].click()
        except TimeoutError:
            print("Error trying to click the video! - {}".format(get_current_time()))
        except:
            print("Error! Could not click the video! - {}".format(get_current_time()))
            browser.quit()
            raise SystemExit

        print("Accessed video {} at {}".format(browser.title, get_current_time()))
    else:
        print("Error: got no videos")
        browser.quit()
        raise SystemExit

    try:
        play_btn = browser.find_elements(By.XPATH, "//button[@class='ytp-play-button ytp-button']")
    except StaleElementReferenceException:
        play_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='ytp-play-button ytp-button']")))
    except TimeoutException:
        play_btn = []

    try:
        shorts_play_btn = browser.find_elements(By.XPATH, "//button[@class='ytp-large-play-button ytp-button']")
    except StaleElementReferenceException:
        shorts_play_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='ytp-large-play-button ytp-button']")))
    except TimeoutException:
        shorts_play_btn = []

    if len(play_btn) == 0 and len(shorts_play_btn) == 0:
        print("Error: did not find the play button - {}".format(get_current_time()))
        browser.quit()
        raise SystemExit
    elif len(play_btn) == 0:
        play_btn = shorts_play_btn[0]
    else:
        play_btn = play_btn[0]
        
    try:
        play_btn.click()
    except StaleElementReferenceException:
        try:
            wait.until(EC.element_to_be_clickable(play_btn))
            play_btn.click()
        except:
            print("Error! Tried pressing play, but failed - {}".format(get_current_time()))
            browser.quit()
            raise SystemExit
    except TimeoutException:
        print("Error! Could not press play button - {}".format(get_current_time()))
        browser.quit()
        raise SystemExit
    except ElementNotInteractableException: 
        print("Error! The button is not interactable - {}".format(get_current_time()))
        browser.quit()
        raise SystemExit

    # browser.execute_script("arguments[0].click()", play_btn)
    print("Pressed play at {}".format(get_current_time()))

    try:
        # Wait for the ad to appear
        skip_ad_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='ytp-ad-skip-button ytp-button']")))

        # Click on the skip ad button
        skip_ad_button.click()
        print("Skipped ad at {}".format(get_current_time()))
    except:
        print("No ad to skip.")

# browser.quit()

def record_screen():
    print("Started recording at {}".format(get_current_time()))

    start_time = time.time()
    duration = 10

    CHUNK = 1024  # Number of samples per frame
    FORMAT = pyaudio.paInt16  # 16-bit int sampling
    CHANNELS = 2  # 2 channels (stereo)
    RECORD_SECONDS = 5
    RATE = 44100  # Sampling rate (frames/second)
    WAVE_OUTPUT_FILENAME = "audio_recording.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    audio_frames = []   


    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        # make a screenshot
        img = pyautogui.screenshot()

        # convert these pixels to a proper numpy array to work with OpenCV
        frame = np.array(img)

        # convert colors from BGR to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # write the frame
        try:
            out.write(frame)
        except IOError:
            print("Error while writting to the .avi file - {}".format(get_current_time))
            raise SystemExit

        data = stream.read(CHUNK)
        audio_frames.append(data)

        # if the user clicks q, it exits
        if cv2.waitKey(1) == ord("q"):
            break

    # make sure everything is closed when exited
    cv2.destroyAllWindows()
    out.release()
    stream.stop_stream()
    stream.close()
    p.terminate()

    print("Finished recording at {}".format(get_current_time()))

    # write to the .wav file
    try:
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(audio_frames))
        wf.close()
    except IOError:
        print("Error while writting to the .wav file - {}".format(get_current_time))
        raise SystemExit

def rms_flat(a):  # from matplotlib.mlab
    """
    Return the root mean square of all the elements of *a*, flattened out.
    """
    return np.sqrt(np.mean(np.absolute(a)**2))


def measure_wav_db_level(wavFile):
    print("Started analyzing the .wav file - {}".format(get_current_time()))

    """
    Open a wave or raw audio file and perform the following tasks:
    - compute the overall level in db (RMS of data)
    """
    try:
        fs, x = wavfile.read(wavFile)
        LOG_SCALE = 20*np.log10(32767)
    except:
        x, fs = sf.read(wavFile,
                        channels=1, samplerate=44100,
                        format='RAW', subtype='PCM_16')
        LOG_SCALE = 0
    t = (np.array(x)).astype(np.float64)
    # x holds the int16 data, but it's hard to work on int16
    # t holds the float64 conversion

    # print(str(fs) + ' Hz')
    # print(str(len(t) / fs) + ' s')
    orig_SPL = 20 * np.log10(rms_flat(t)) - LOG_SCALE
    # print('Sound level:   ' + str(orig_SPL) + ' dBFS')

    f = open("out.txt", "w")
    f.write('Sound level:   ' + str(orig_SPL) + ' dBFS')

    return orig_SPL

if __name__ == '__main__':
    if is_connected():
        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        wait = WebDriverWait(browser, 10)

        open_youtube(browser, wait)
        play_video(browser, wait)

        record_screen()
        measure_wav_db_level("audio_recording.wav")

        browser.quit()
        print("Closed browser at {}".format(get_current_time()))
    else:
        print("Error! No interner connection")
        raise SystemExit