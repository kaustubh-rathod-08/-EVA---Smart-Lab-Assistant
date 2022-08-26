import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import pyaudio
import ctypes
from operator import add
import socket
import psutil
import platform

flag = 0

if_addrs = psutil.net_if_addrs()
for interface_name, interface_addresses in if_addrs.items():
    if interface_name == "Wi-Fi":
        for address in interface_addresses:
            if str(address.family) == 'AddressFamily.AF_INET':
                serverip = address.address
net_io = psutil.net_io_counters()
s = socket.socket()
s.bind((serverip,9999))
s.listen(3)

assistant =pyttsx3.init("sapi5")
voices = assistant.getProperty("voices")
rate = assistant.getProperty('rate')
assistant.setProperty('rate', rate-30)
assistant.setProperty("voice", voices[1].id)
problem = ""

def speak(sound):
    assistant.say(sound)
    assistant.runAndWait()

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def order():
    read = sr.Recognizer()
    with sr.Microphone() as source:
        print("\tListening... 🎙️")
        read.pause_threshold = 0.8
        read.energy_threshold = 500
        sound = read.listen(source)
    try:
        print("\tRecognising... 💭")
        problem = read.recognize_google(sound, language='en-in')
        print(f"\tI heard {problem}\n")
        
    except Exception:
        print(Exception)
        print("\n\tPardon me, I was unable to understand could you Please repeat...")
        speak("Pardon me, I was unable to understand could you please repeat")
        return "None"
    return problem

def greeting():
    print("\n\n\n\n\n")
    print(
"\t\t\t\t\t\t\t\t\t███████╗██╗   ██╗ █████╗ \n"
"\t\t\t\t\t\t\t\t\t██╔════╝██║   ██║██╔══██╗\n"
"\t\t\t\t\t\t\t\t\t█████╗  ╚██╗ ██╔╝███████║\n"
"\t\t\t\t\t\t\t\t\t██╔══╝   ╚████╔╝ ██╔══██║\n"
"\t\t\t\t\t\t\t\t\t███████╗  ╚██╔╝  ██║  ██║\n"
"\t\t\t\t\t\t\t\t\t╚══════╝   ╚═╝   ╚═╝  ╚═╝\n")
    print("\t\t\t\t\t\t\t\t\t     𝕿𝖍𝖊 𝕷𝖆𝖇 𝕬𝖘𝖘𝖎𝖘𝖙𝖆𝖓𝖙")
    time = int(datetime.datetime.now().hour)
    
    if time>=0 and time<12:
        speak("Good Morning Everyone")
    elif time>=12 and time<18:
        speak("Good Afternoon everyone")
    else:
        speak("Good Evening everyone")
   
def server_connection():
    global flag
    while True:
        speak("Do you wish to connect your pc to this server ?")
        cmd2 = input("\t► Do you wish to connect your pc to this server ? (yes / no): ")
        cmd2 = cmd2.lower()
        if cmd2 == "yes":
            speak("initializing server")
            if_addrs = psutil.net_if_addrs()
            for interface_name, interface_addresses in if_addrs.items():
                if interface_name == "Wi-Fi":
                    for address in interface_addresses:
                        if str(address.family) == 'AddressFamily.AF_INET':
                            print(f"\t► Enter the IP Address : ({address.address}) in your Client PC")
                            speak ("Enter the above IP Address in your client pc")
            net_io = psutil.net_io_counters()
            print("\tWaiting for connections...🕑")
            speak ("Waiting for connections...")
            global c, addr
            c, addr = s.accept()
            name = c.recv(1024).decode()
            print (f"\tConnected with {name} ✅")
            speak (f"connected with {name}")
            flag = 0
            break
        elif cmd2 == "no":
            print("\tStarting offline mode 📴")
            flag = 1
            speak("continuing to offline mode")
            break
        else:
            print("\tEnter valid command ❌")

def check_command(problem):
    if "client status" in problem:
        print("\tContacting client ⟳")
        try:
            c.send(bytes("status",'utf-8'))
            print("\tClient is online ✅")
            speak("Client is online")
        except Exception:
            print("\tClient is offline ❌")
            speak("unable to connect to client is offline, it seems clients is offline")

    elif "client" in problem:
        if flag == 0:
            print("\tContacting client ⟳")
            try:
                c.send(bytes(problem,'utf-8'))
                print("\tSending Query to Client...")
                speak("Sending Query to Client")
            except Exception:
                print("\tClient is offline ❌")
                speak("unable to connect to client is offline, it seems clients is offline")
        elif flag == 1:
            print ("\tServer is in offline mode 📴")
            speak ("Server is in offline mode")
            speak ("Would you like to setup online mode")
            while True:   
                cmd3 = input("\t► Would you like to setup online mode? (yes / no): ")
                cmd3=cmd3.lower()
                if cmd3 == "yes":
                    server_connection()
                elif cmd3 == "no":
                    print("\tContinuing to offline mode 📴")
                    speak("continuing to offline mode")
                    text_command()
                else:
                    print("Enter valid command ❌")

    elif "wikipedia" in problem:
        print("\tSearching on the Wikipedia 🔍")
        speak("Searching on the wikipedia... ")
        result = wikipedia.summary(problem, sentences=2)
        print("\t• Here's what I found, " + result)
        speak("Here's what I found, ")
        speak(result)
    
    elif "get information" in problem:
        speak ("just a second , collecting the system data")

        #System Information
        print("="*40, "System Information", "="*40)
        uname = platform.uname()
        print(f"\n    \u2022 System: {uname.system}")
        print(f"    \u2022 Node Name: {uname.node}")
        print(f"    \u2022 Release: {uname.release}")
        print(f"    \u2022 Version: {uname.version}")
        print(f"    \u2022 Machine: {uname.machine}\n")

        #Network Information
        print("-"*40, "Network Information", "-"*40)
        if_addrs = psutil.net_if_addrs()
        for interface_name, interface_addresses in if_addrs.items():
            if interface_name == "Wi-Fi":
                for address in interface_addresses:
                    if str(address.family) == 'AddressFamily.AF_INET':
                        print(f"    \u2022 IP Address: {address.address}")
                        print(f"    \u2022 Netmask: {address.netmask}")
                        print(f"    \u2022 Broadcast IP: {address.broadcast}")
        net_io = psutil.net_io_counters()

        # CPU information
        print("-"*40, "CPU Information", "-"*40)
        print("    \u2022 Physical cores:", psutil.cpu_count(logical=False))
        print("    \u2022 Total cores:", psutil.cpu_count(logical=True))
        print(f"    \u2022 Max Frequency: {psutil.cpu_freq().max:.2f}Mhz")
        print(f"    \u2022 Current Frequency: {psutil.cpu_freq().current:.2f}Mhz")
        print(f"    \u2022 Total CPU Usage: {psutil.cpu_percent()}%")

        # Memory Information
        print("-"*40, "Memory Information", "-"*40)
        svmem = psutil.virtual_memory()
        print(f"    \u2022 Total: {get_size(svmem.total)}")
        print(f"    \u2022 Available: {get_size(svmem.available)}")
        print(f"    \u2022 Used: {get_size(svmem.used)}")
        print(f"    \u2022 Percentage: {svmem.percent}%")


        # Disk Information
        print("-"*40, "Disk Information", "-"*40)
        partitions = psutil.disk_partitions()
        for partition in partitions:
            print(f"        # Device: {partition.device}")
            print(f"    \u2022 File system type: {partition.fstype}")
            partition_usage = psutil.disk_usage(partition.mountpoint)
            print(f"    \u2022 Total Size: {get_size(partition_usage.total)}")
            print(f"    \u2022 Used: {get_size(partition_usage.used)}")
            print(f"    \u2022 Free: {get_size(partition_usage.free)}")
            print(f"    \u2022 Percentage Used: {partition_usage.percent}%")

    elif "open youtube" in problem:
        webbrowser.open("youtube.com")
        speak ("opening youtube")
    elif "open google" in problem:
        webbrowser.open("google.com")
        speak ("opening google")
    elif "open stack overflow" in problem:
        webbrowser.open("stackoverflow.com")
        speak ("opening stack overflow")
    elif "open classroom" in problem:
        webbrowser.open("https://classroom.google.com/h")
        speak ("opening google classroom")
        speak ("I guess submission dead lines are near.")

    elif "shutdown" in problem:
        print("\tShutting down the PC 🖥️")
        speak("Shutting down the PC in 5 seconds")
        webbrowser.os.system("shutdown /s /t 5")
    elif "restart" in problem:
        print("\tRestarting the PC 🖥️")
        speak("restarting the PC in 5 seconds")
        webbrowser.os.system("shutdown /r /t 5")
    elif "lock" in problem:
        print("\tLocking the PC 🖥️")
        speak("okay locking the PC...")
        ctypes.windll.user32.LockWorkStation()
    
    elif "open vs code" in problem:
        vsCode= "C:\\Users\\sarth\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
        webbrowser.os.startfile(vsCode)
        speak ("opening V S code")
    elif "open word" in problem:
        word= "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE"
        webbrowser.os.startfile(word)
        speak ("opening M S word")

    elif "today" in problem:
        day = int(datetime.datetime.today().weekday())
        weekdays= ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        print(f"\tToday is {weekdays[day]} 📅")
        speak(f"Today is {weekdays[day]}")
    elif "time" in problem:
        strTime = datetime.datetime.now().strftime("%H : %M")
        print(f"\tThe time is {strTime} 🕑")
        speak(f"The time is {strTime}")
    elif "take a break" in problem:
        quit()
    else:
        print ("\tPlease, Enter a valid command ❌")
        speak ("please, enter a valid command")

def voice_command():
    problem = order().lower()
    check_command(problem)

def text_command():
    problem = str(input("\t► Enter the command : "))
    problem = problem.lower()
    check_command(problem)
greeting()
server_connection()
while True:
    cmd = input("\t► Do you wish to give voice command to your computer ? (yes / no): ")
    cmd = cmd.lower()
    if cmd == "yes":
        while True:
            voice_command()
    elif cmd == "no":
        while True:
            text_command()
    else:
        print("\tEnter valid command ❌")