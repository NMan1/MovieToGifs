import glob
import ntpath
import os
import time
import requests
import srt as srt
from moviepy.editor import VideoFileClip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


save_count = 1


def send_gif(token, channel_id, path, msg):
    url = f"https://discord.com/api/v8/channels/{channel_id}/messages"

    headers = {
        "authorization": token,
        'Expect': 'application/json',
    }

    files = {
        'file': (ntpath.basename(path), open(path, 'rb')),
        'payload_json': (None, '{ "wait": true, "content": "' + msg + '" }'),
    }

    r = requests.post(url, headers=headers, files=files)
    if r.status_code == 200:
        print("Upload to discord success \n")
    else:
        print("Upload to discord failed \n")


def upload_mp4(path):
    driver.find_element_by_id("new-image").send_keys(os.getcwd() + "/movie/out.mp4")
    driver.find_element_by_css_selector('input[name="upload"]').click()
    time.sleep(2)
    WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="video-to-gif"]'))).click()


def upload_convert_video(path):
    global save_count
    upload_mp4(path)

    try:
        WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#output .save'))).click()
    except Exception:
        driver.get("https://ezgif.com/video-to-gif")
        upload_mp4(path)
        WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#output .save'))).click()

    while True:
        try:
            os.rename("gifs/ezgif.com-video-to-gif.gif", f"gifs/{str(save_count)}.gif")
            break
        except Exception:
            pass

    print(f"Saved gif: {save_count}.gif")
    driver.get("https://ezgif.com/video-to-gif")


def start_driver():
    url = "https://ezgif.com/video-to-gif"
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {"download.default_directory":  os.getcwd() + '\\gifs', "download.prompt_for_download": False, "download.directory_upgrade": True})
    temp = webdriver.Chrome("C:\\chromedriver.exe", chrome_options=options)
    temp.get(url)
    return temp


if __name__ == '__main__':
    # Create driver object
    driver: webdriver.Chrome = start_driver()

    # Find starting index if stopped before finishing
    list_of_files = glob.glob('gifs/*')
    skip_number = 0
    if len(list_of_files) > 0:
        latest_file = max(list_of_files, key=os.path.getctime)
        skip_number = int(ntpath.basename(latest_file).replace(".gif", ""))

    # Dynamically find movie file
    movie_files = glob.glob('movie/*.mp4')
    movie_file_name = ""
    for file in movie_files:
        if ntpath.basename(file) != "out.mp4":
            movie_file_name = file

    # Parse captions file
    subs = list(srt.parse(open(glob.glob('movie/*.srt')[0])))
    for index, sub in enumerate(subs):
        # Skip already created clips if applicable
        if index < skip_number:
            save_count += 1
            continue

        # Create move clip
        clip = VideoFileClip(movie_file_name).subclip(sub.start.total_seconds(), sub.end.total_seconds())
        clip.to_videofile("movie/out.mp4", codec="libx264", temp_audiofile='temp-audio.m4a', remove_temp=True,
                          audio_codec='aac', verbose=False, logger=None)

        # Convert to gif
        print(f"Created clip: {save_count} from {str(sub.start)} -> {str(sub.end)}")
        upload_convert_video("movie/out.mp4")

        # Uncomment to send to discord channel
        # send_gif("token", channel_id, f"gifs/{str(save_count)}.gif", f"Created gif: {save_count} from {str(sub.start)} -> {str(sub.end)}")

        save_count += 1

    # Stop
    driver.close()
    driver.quit()