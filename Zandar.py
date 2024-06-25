import pyttsx3
import speech_recognition as sr
import json
import time
import random
import pyautogui
import datetime
import logging
import webbrowser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pywhatkit
import pytube
import pyperclip
import socket
import os
import ctypes
from sentence_transformers import SentenceTransformer, util
import spacy
import requests
from difflib import SequenceMatcher
import shutil
import psutil
import pyjokes
import subprocess
import platform
from pywinauto import application



#pyttsx3 Engine
engine=pyttsx3.init('sapi5') 
engine.setProperty('volume', 1)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

#Chrome driver path
chromedriver= r"C:\Users\Mohammed Uzair\OneDrive\Desktop\Python Projects\chromedriver.exe" 
#Ck&sHQA?epi9(@TP

class Device:  # Device Operations
    #I/O Functions
    @staticmethod
    def speak(audio):
        engine.say(audio)
        engine.runAndWait()

    @staticmethod
    def TakeCommand():
        r = sr.Recognizer()
        with sr.Microphone() as source :
            print("Listening..")
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, timeout=300, phrase_time_limit=20)
        
        try:
            print("Recognizing..")
            query = r.recognize_google(audio, language='en-US' )
            print(query)

        except Exception as e:
            return "None"
        return query
    
    @staticmethod
    def std_response(key):
        file = open(r"C:\Users\Mohammed Uzair\OneDrive\Desktop\Python Projects\NLP - UI\Zandar\Basic Responses.txt", 'r')
        contents = file.read()
        my_dict = json.loads(contents)
        response_list = my_dict[key]
        response = random.choice(response_list)
        Device.speak(response)

    @staticmethod
    def Initiate():
        print("Initializing..")
        #time.sleep("Copying query files...")
        Device.Copy_Script_Files()
        #time.sleep(1)
        #Device.speak("initializing sequence complete")
        print("Initialzing Sequence Complete\nSystems Online")
        hour = datetime.datetime.now().hour
        if hour>=5 and hour<12:
            Device.speak("good morning uzi")
            Device.std_response('start_up')
        elif hour>=12 and hour<16:
            Device.speak("good afternoon uzi")
            Device.std_response('start_up')
        elif hour>=16 and hour<20:
            Device.speak("good evening uzi")
            Device.std_response('start_up')
        else:
            Device.speak("welcome uzi, what can i do for you?")

    @staticmethod
    #To call required function as string
    def Execute(func, arg):
        getattr(Actions, func)(arg)

    # Copying all query txt files incase they get corrupted during execution
    @staticmethod
    def Copy_Script_Files():
        files = ["C:\\Users\\Mohammed Uzair\\OneDrive\\Desktop\\Python Projects\\NLP - UI\\Zandar\\Basic Responses.txt", 
                "C:\\Users\\Mohammed Uzair\\OneDrive\\Desktop\\Python Projects\\NLP - UI\\Zandar\\Queries.txt",
                "C:\\Users\\Mohammed Uzair\\OneDrive\\Desktop\\Python Projects\\NLP - UI\\Zandar\\Tags.txt"]
        for source_file in files:
            # Extract the filename from the source file path
            filename = source_file.split("\\")[-1]
            destination_folder = 'C:\\Users\\Mohammed Uzair\\OneDrive\\Documents\\Zandar Back Up'
            # Create the destination file path by joining the destination folder and the filename
            destination_file = os.path.join(destination_folder, filename)
            # Copy the file
            shutil.copy(source_file, destination_file)
        # Copy the file
        shutil.copy(source_file, destination_file)

    @staticmethod
    def GetRunningApps():
        running_apps = []
        for process in psutil.process_iter(attrs=['pid', 'name']):
            try:
                process_info = process.info
                if process_info['name']:
                    running_apps.append(process_info['name'])
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return list(set(running_apps))  #set to remove duplicates
    
    @staticmethod
    def GetOpenWifi():
        system_platform = platform.system()
        open_wifi_networks = []

        if system_platform == "Windows":
            try:
                # Run the Windows 'netsh' command to list Wi-Fi networks
                result = subprocess.run(["netsh", "wlan", "show", "network"], capture_output=True, text=True, check=True)
                output = result.stdout

                # Parse the output to extract open Wi-Fi network information
                lines = output.splitlines()
                ssid = None
                for line in lines:
                    if "SSID" in line:
                        ssid = line.split(":")[1].strip()
                    elif "Authentication" in line:
                        auth_type = line.split(":")[1].strip()
                        if "Open" in auth_type:
                            open_wifi_networks.append(ssid)

            except subprocess.CalledProcessError as e:
                print("Error:", e)
        
        elif system_platform == "Linux":
            try:
                # Run the Linux 'nmcli' command to list Wi-Fi networks (NetworkManager)
                result = subprocess.run(["nmcli", "-f", "SSID,SECURITY", "device", "wifi", "list"], capture_output=True, text=True, check=True)
                output = result.stdout

                # Parse the output to extract open Wi-Fi network information
                lines = output.splitlines()
                for line in lines[1:]:
                    ssid, security = line.strip().split()
                    if security.lower() == "none":
                        open_wifi_networks.append(ssid)

            except subprocess.CalledProcessError as e:
                print("Error:", e)
        return open_wifi_networks
    
    def Ambient_Mode(cur_pos):
        if cur_pos == 'on':
            file = open(r"C:\Users\Mohammed Uzair\OneDrive\Desktop\Python Projects\NLP - UI\Zandar\Ambient Mode.txt", 'w')
            file.writelines(['1'])
            file.close()
        else:
            file = open(r"C:\Users\Mohammed Uzair\OneDrive\Desktop\Python Projects\NLP - UI\Zandar\Ambient Mode.txt", 'w')
            file.writelines(['0'])
            file.close()
            


class Query: # Query Operations 
    #To get cosine similarity
    @staticmethod
    def Built_in_Sim(a, b):
        return SequenceMatcher(None, a, b).ratio()
    
    #Getting similarity score
    def GetSimScore(query):
        flag = 0
        model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        file = open(r"C:\Users\Mohammed Uzair\OneDrive\Desktop\Python Projects\NLP - UI\Zandar\Tags.txt", 'r')
        contents = file.read()
        data = json.loads(contents)
        for sim_query in data.keys():
            embedding1 = model.encode(query, convert_to_tensor=True)
            embedding2 = model.encode(sim_query, convert_to_tensor=True)
            # Calculate cosine similarity between embeddings
            cosine_similarity = util.pytorch_cos_sim(embedding1, embedding2)
            sm_similarity = Query.Built_in_Sim(query, sim_query)
            if cosine_similarity > 0.8 or sm_similarity>0.9:
                flag = 1
                print("Similar query:", sim_query)
                #assigning tag and key of similar query
                tag, key = Query.AssignTag(sim_query)
                print(f"Tag: {tag}\nKey: {key}")
                return tag, key, sim_query, flag
        return None, None, None, flag  #check if working
            
            

    #To write into Tags.txt after getting sim score
    @staticmethod
    def CreateTag(query, tag, sim_query):
        file_path = r"C:\Users\Mohammed Uzair\OneDrive\Desktop\Python Projects\NLP - UI\Zandar\Tags.txt"
        file = open(file_path, 'r')
        contents = file.read()
        data = json.loads(contents)
        file.close()
        new_data = {f'{query}': f'{tag}'}
        print('new tags data:', new_data)
        data.update(new_data)
        file = open(file_path, 'w')
        json.dump(data, file, indent=4)
        file.close()
        Query.WriteQuery(query, tag, sim_query)
        
    #To write into Queries.txt or Basic Responses.txt 
    @staticmethod
    def WriteQuery(query, tag, sim_query):
        try:
            if tag == 'action':
                file_path = r"C:\Users\Mohammed Uzair\OneDrive\Desktop\Python Projects\NLP - UI\Zandar\Queries.txt"
            elif tag == 'basic':
                file_path = r"C:\Users\Mohammed Uzair\OneDrive\Desktop\Python Projects\NLP - UI\Zandar\Basic Responses.txt"
            file = open(file_path, 'r')
            contents = file.read()
            data = json.loads(contents)
            file.close()
            new_data = {f'{query}': f'{data[sim_query]}'}
            print('new query data:', new_data)
            data.update(new_data)
            file = open(file_path, 'w')
            json.dump(data, file, indent=4)
            file.close()
        except:
            print(f"Can't assign file for {tag} tag")
    
    #To see execute the similar query
    def MatchQuery(query):
        try:
            tag, key, sim_query, flag = Query.GetSimScore(query)
            if flag==1:
                Query.Evaluate(sim_query, tag, key)
                print("Learning..")
                Query.CreateTag(query, tag, sim_query)
                print("Query added!")
            else:
                print("No similar query found")
                if Actions.Ambience(query) == True:
                    print("Ambient Mode is on...")
                else:
                    Device.speak("Here's what i found on the web")
                    print("Redirecting to Google...")
                    pywhatkit.search(query)
        except Exception as e:
            print(f"Error: {e}\nNone type input has not been handled!")


    @staticmethod
    def AssignTag(query):
        file = open(r"C:\Users\Mohammed Uzair\OneDrive\Desktop\Python Projects\NLP - UI\Zandar\Tags.txt", 'r')
        contents = file.read()
        data = json.loads(contents)
        keys = data.keys()
        for key in keys:
            try:
                if key in query:  # Check if keyword exists in query
                    return data[key], key  # Return tag to open specific file and key to access required value in dictionary
            except Exception as e:            
                logging.error("Tag does not exist", exc_info=True)
        return "Unassigned", None

    @staticmethod
    def Evaluate(query, tag, key=None):
        if tag == 'basic':
            file = open(r"C:\Users\Mohammed Uzair\OneDrive\Desktop\Python Projects\NLP - UI\Zandar\Basic Responses.txt", 'r')
            contents = file.read()
            data = json.loads(contents)
            Device.speak(data[key])
            file.close()

        elif tag == 'action':
            file = open(r"C:\Users\Mohammed Uzair\OneDrive\Desktop\Python Projects\NLP - UI\Zandar\Queries.txt", 'r')
            contents = file.read()
            data = json.loads(contents)
            func = data[key] # Gets function name(value) from dictionary
            print(f"executing {func}()")
            Device.Execute(func, query)
            file.close()
            Device.std_response('follow_up')

        elif tag == 'Unassigned':
            Query.MatchQuery(query)

            
class Actions:   # Response Operations
    #Opening apps, websites etc
    @staticmethod
    def open_application(query):
        site_dict = {"youtube music":"music.youtube.com", "reddit": "reddit.com", "gmail": "gmail.com"}
        app = query.replace('open ', '',1)
        if app in site_dict.keys():
                Device.speak(f"opening {app}")
                webbrowser.register('chrome', None, webbrowser.BackgroundBrowser("C:\Program Files\Google\Chrome\Application\chrome.exe"))
                webbrowser.get('chrome').open(site_dict[app])

        elif '.' in app:
            url = app
            Device.speak(f"opening {app}")
            webbrowser.register('chrome', None, webbrowser.BackgroundBrowser("C:\Program Files\Google\Chrome\Application\chrome.exe"))
            webbrowser.get('chrome').open(url)

        #Handling Collision with ShowOpenNetworks
        elif "network" in app:
            print("Switching function to ShowOpenNetworks...")
            Actions.ShowOpenNetworks()

        else:
            app = query.replace('open ', '',1)
            Device.speak(f"opening {app}")
            pyautogui.press('winleft')
            time.sleep(1)
            pyautogui.typewrite(app)
            time.sleep(2)
            pyautogui.press('enter')

    #Only works in .exe applications
    @staticmethod
    def close_application(query):
        running_apps = Device.GetRunningApps()
        query_lst = query.split()
        if len(query_lst) <= 4 and len(query_lst)>1:
            app = query_lst[len(query_lst)-1]
            executable = app + ".exe"
            if executable in running_apps or executable.capitalize() in running_apps:
                Device.speak(f"closing {app}")
                print(executable)
                os.system(f"taskkill /f /im {executable}")
            else:
                print(f"No executable file found for {app}")
                Device.speak(f"An error occured while terminating {app}")
        else:
            print("Redirecting to spotify..")
            Actions.spotify_control(query) #incase close is part of a song
    
    #Edit when you figure out how add dynamic query to json file. Works only for specified query in tag.txt
    @staticmethod
    def spotify_control(command):
        if command=='play some music' or command== 'play some tunes' or command== 'play music':
            Device.speak("asking spotify to play some music")
            pyautogui.press('winleft')
            time.sleep(1)
            pyautogui.typewrite('spotify')
            time.sleep(3)
            pyautogui.press('enter')
            time.sleep(4)
            pyautogui.press('space')
        else:    
            sub_query1=command.replace('can you play','')
            sub_query2=sub_query1.replace('on spotify','')
            sub_query3=sub_query2.replace('by','', 1)
            song_name=sub_query3.replace('play','', 1).strip()
            if song_name == 'some music':
                Actions.spotify_control('play some music')
            else:
                Device.speak(f"playing {song_name} on spotify")
                print("song name:", song_name)
                pyautogui.press('winleft')
                time.sleep(1)
                pyautogui.typewrite('spotify')
                time.sleep(3)
                pyautogui.typewrite(['enter'])
                time.sleep(4)
                pyautogui.click(x=90, y=114)
                time.sleep(1)
                pyautogui.click(x=539, y=72)
                time.sleep(1)
                pyautogui.click(x=539, y=72)
                time.sleep(1)
                pyautogui.typewrite(song_name)
                time.sleep(3)
                pyautogui.moveTo(x=643, y=400)
                time.sleep(1.5)
                pyautogui.click(x=643, y=400)
    
    @staticmethod
    def ShowOpenNetworks():
        open_networks = Device.GetOpenWifi()
        if open_networks:
            Device.speak("i found the following open networks in your vicinity")
            print("Open Wi-Fi Networks:")
            for i in open_networks:
                print(f"{open_networks.index(i)+1}. {i}")
        else:
            Device.speak("there are no open networks availible in your vicinity")

    #Fetching current location using api
    def get_location(self):
        try:
            Device.speak("fetching current location")
            ipAdd = requests.get("https://api.ipify.org").text
            url = 'https://get.geojs.io/v1/ip/geo/'+ipAdd+'.json'
            geo_requests=requests.get(url)
            geo_data=geo_requests.json()
            city=geo_data['city']
            country=geo_data['country']
            Device.speak(f"we are in {city} city {country}")
        except Exception as e:
            Device.speak("Unable to fetch current location due to network error")
            print("Error:", e)

    def Time(self):   # Needs an argument since Device.Execute take 1 mandatory
        time_str = datetime.datetime.now().strftime("%I:%M:%p")
        print(time_str)
        time_now = time_str.replace(':','')
        Device.speak("it is")
        Device.speak(time_now)

    def date(self):
        today = datetime.datetime.now().strftime('%d:%B:%Y')
        f_date=today.replace(':',' ')
        print(f_date)
        Device.speak("today's date is")
        Device.speak(today)

    #Weather info using api
    def weather(self):
        try:
            api_address = 'http://api.openweathermap.org/data/2.5/weather?q=Bengaluru&appid=c5f055850f8a240d35849e8ea7d2c66b'
            json_data = requests.get(api_address).json()
            tem=json_data['main']['temp']
            temp=round(tem-273)
            wind= json_data['wind']['speed']
            des=json_data['weather'][0]['description']
            Device.speak(f'the weather in Bangalore is {temp} degrees celcius with a {des} and wind speeds of {wind} kilometer per hour.')
        except:
            Device.speak("I detect a code malfunction in weather function, please check and try again")

    def ClownMF():
        joke = pyjokes.get_joke()
        Device.speak("here's a joke.")
        Device.speak(joke)
        Device.speak("haha")
   

    #Downloads any video asked by user
    def yt_downloader(self):
        Device.speak("what is the title of the video?")
        video_title = Device.TakeCommand().lower()
        pywhatkit.playonyt(video_title)
        time.sleep(2)
        pyautogui.press('playpause')
        Device.speak("is this the video you want to download?")
        res = Device.TakeCommand().lower()
        if 'yes' in res or 'yeah' in res or 'ya' in res:
            pyautogui.hotkey('ctrl', 'l')
            time.sleep(.5)
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(.5)
            pyautogui.hotkey('ctrl', 'w')
            pyautogui.hotkey('winleft', '4')
            url = pyperclip.paste()
            video = pytube.YouTube(url)
            stream=video.streams.get_by_itag(22)
            Device.speak(f"Downloading {video.title}, please wait.")
            try:
                stream.download(r"C:\Users\Mohammed Uzair\OneDrive\Desktop\Youtube Downloads")
                print(f"{video.title} downloaded successfully")
                Device.speak("video download complete. file stored in youtube downloads folder on desktop")
            except:
                Device.speak("download unsuccessful, Video is not availible for specified  i-tag")
        else:
            Device.speak("download procedure aborted")

    #Fetching IP Address using built in funcs
    def get_ip(self):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        print(f"Your IP Address is: {ip}")
        Device.speak(f"you ip address is {ip}")

    def Ambience(query):
        file=open(r"C:\Users\Mohammed Uzair\OneDrive\Desktop\Python Projects\NLP - UI\Zandar\QWC.txt", 'a+')
        file.seek(0)
        lines = file.readlines()
        line_count = len(lines)
        q = f"{line_count}. {query}"
        file.write('\n'+ q)
        file.close()
        qwc_file=open(r"C:\Users\Mohammed Uzair\OneDrive\Desktop\Python Projects\NLP - UI\Zandar\Ambient Code.txt",'r')
        r=qwc_file.readline()
        if r=='0':
            return False
        elif r=='1':
            return True
        qwc_file.close

    #Controls shutting down, restarting, locking pc and others
    def system_control(arg):
        if 'shutdown' in arg or 'power down' in arg or 'power off' in arg or 'turn off' in arg:
             pyautogui.hotkey('ctrl', 's')
             os.system("shutdown /s /t 1")

        elif 'volume up' in arg or 'increase' in arg:
            pyautogui.press('volumeup', presses=5)

        elif 'volume down' in arg or 'decrease' in arg:
            pyautogui.press('volumedown', presses=5)
        
        elif 'reboot' in arg or 'restart' in arg:
            Device.speak("rebooting console")
            pyautogui.hotkey('ctrl', 's')
            print("Restarting...")
            time.sleep(1)
            os.system("shutdown /r /t 1")

        elif 'lock' in arg:
            Device.speak("locking workstation")
            print("Locking PC...")
            ctypes.windll.user32.LockWorkStation()

        elif 'screenshot' in arg:
            pyautogui.hotkey('winleft', 'prtsc')
            Device.speak("screenshot saved in folder")

        elif 'switch' in arg:
            if arg == 'switch window' or arg == 'swipe' or arg == 'change window':
                pyautogui.keyDown("alt")
                pyautogui.press('tab')
                pyautogui.keyUp('alt')
            
            else:
                pass
            
        elif 'minimise' in arg or "home" in arg:
            pyautogui.hotkey('winleft','m')

        else:
            Device.speak("command functionality does not exist")
            print("Check system_control()")

# Query Evaluation
Device.Initiate()
while True:
    query = input("Query: ")
    #query = Device.TakeCommand().lower()
    print(f"query: {query}")
    tag, key = Query.AssignTag(query)
    print(f"Tag: {tag}\nKey: {key}")
    Query.Evaluate(query, tag, key)
