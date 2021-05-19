import os
import time
import pyautogui
import speech_recognition as sr
from pydub import AudioSegment
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

ADDRESS = "DQ1nX7KrmGngLnpuyQVu46X3EF4vH3UkLx"
num = 1

class DogeCoin:
    def __init__(self):
        options = Options()
        options.add_argument("window-size=1300,600")
        options.add_extension("extensions/cjpalhdlnbpafiamejdnhcphjbkeiagm.crx")
        self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.wait = WebDriverWait(self.browser, 15)
        self.browser.delete_all_cookies()

    def start_browser(self):
        self.browser.get("https://dogebuzz.com/")
        time.sleep(2)
        enter_address = self.wait.until(EC.element_to_be_clickable((By.NAME, "address")))
        enter_address.send_keys(ADDRESS)
        claim = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[type='submit']")))
        claim.click()

    def claim(self):
        claim = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[type='submit']")))
        self.browser.execute_script("arguments[0].scrollIntoView();", claim)
        time.sleep(2)
        claim.click()
        self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
        time.sleep(2)
        captcha = self.wait.until(EC.element_to_be_clickable((By.ID, "recaptcha-anchor")))
        self.browser.execute_script("arguments[0].scrollIntoView();", captcha)
        time.sleep(1.5)
        captcha.click()
        # time.sleep(3)
        self.browser.switch_to.default_content()
        self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[name^='c-'][src^='https://www.google.com/recaptcha/api2/bframe?']")))
        time.sleep(3)
        buster_captcha = self.wait.until(EC.element_to_be_clickable((By.ID, "recaptcha-audio-button")))
        buster_captcha.click()
        self.solve_captcha()

    def solve_captcha(self):
        try:
            download = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[class="rc-audiochallenge-tdownload-link"]')))
            actionChains = ActionChains(self.browser)
            actionChains.context_click(download).perform()
            time.sleep(1)
            pyautogui.press("down", presses=4)
            pyautogui.press("enter")
            time.sleep(2)
            pyautogui.typewrite(f"{os.getcwd()}\\Downloads\\audio.mp3", interval=0.01)
            pyautogui.press("enter")
            pyautogui.press(["left", "enter"])
            time.sleep(3)
            self.convert_to_wav()
            captcha_text = self.audio_to_text()
            cap = self.wait.until(EC.element_to_be_clickable((By.ID, "audio-response")))
            cap.send_keys(captcha_text)
            time.sleep(1)
            verify = self.wait.until(EC.element_to_be_clickable((By.ID, "recaptcha-verify-button")))
            verify.click()
            self.browser.switch_to.default_content()
            time.sleep(1)
            claim2 = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[type='submit']")))
            claim2.click()
            self.browser.save_screenshot(f"screenshots/{num}.png")
        except (TimeoutException, ElementClickInterceptedException):
            self.wait.until(EC.frame_to_be_available_and_switch_to_it(
                (By.CSS_SELECTOR, "iframe[name^='c-'][src^='https://www.google.com/recaptcha/api2/bframe?']")))
            self.solve_captcha()

        else:
            self.go_on()


    def go_on(self):
        self.browser.refresh()
        self.claim()
        time.sleep(2)

    def audio_to_text(self):
        r = sr.Recognizer()
        harvard = sr.AudioFile('Downloads/audio.wav')
        with harvard as source:
            audio = r.record(source)
            text = r.recognize_google(audio)
            print(text)
            return text

    def convert_to_wav(self):
        sound = AudioSegment.from_mp3("Downloads/audio.mp3")
        sound.export("Downloads/audio.wav", format="wav")



def main():
    claim = DogeCoin()
    claim.start_browser()
    claim.claim()


if __name__ == '__main__':
    main()
