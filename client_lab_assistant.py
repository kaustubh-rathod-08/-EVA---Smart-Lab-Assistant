import datetime
import wikipedia
import webbrowser
import ctypes
import pyttsx3
from operator import add
import socket
import psutil
import platform
import datetime

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor
print ("\t•Note: This server is requesting access and control of the Python Application.")
print ("\t       Allow access only if you trust the server, Enter IP below to grant access.")
c = socket.socket()

while True:
    try:
        serverip = input("\t►Enter the IP Address of the server :")
        c.connect((serverip,9999))
        print("Server connected ✅")
        break
    except Exception:
        print("\tEnter valid IP address")
name = "client"
c.send(bytes(name,'utf-8'))

while True:
    problem = c.recv(1024).decode()
    print (problem)
    if "status" in problem:
        print("\tSending status to server")
    elif "wikipedia" in problem:
        print("\tSearching on the Wikipedia 🔍")
        result = wikipedia.summary(problem, sentences=2)
        print("\t• Here's what I found, " + result)
    
    elif "get information" in problem:

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
    elif "open google" in problem:
        webbrowser.open("google.com")
    elif "open stack overflow" in problem:
        webbrowser.open("stackoverflow.com")
    elif "open classroom" in problem:
        webbrowser.open("https://classroom.google.com/h")

    elif "shutdown" in problem:
        print("\tShutting down the PC 🖥️")
        webbrowser.os.system("shutdown /s /t 5")
    elif "restart" in problem:
        print("\tRestarting the PC 🖥️")
        webbrowser.os.system("shutdown /r /t 5")
    elif "lock" in problem:
        print("\tLocking the PC 🖥️")
        ctypes.windll.user32.LockWorkStation()
    
    elif "open vs code" in problem:
        vsCode= "C:\\Users\\sarth\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
        webbrowser.os.startfile(vsCode)
    elif "open word" in problem:
        word= "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE"
        webbrowser.os.startfile(word)

    elif "today" in problem:
        day = int(datetime.datetime.today().weekday())
        weekdays= ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        print(f"\tToday is {weekdays[day]} 📅")
    elif "time" in problem:
        strTime = datetime.datetime.now().strftime("%H : %M")
        print(f"\tThe time is [{strTime}] 🕑")
    elif "take a break" in problem:
        quit()