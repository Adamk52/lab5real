import subprocess
import sys

def installMongo(): # installs mongo db 
    try:
        lsb_release = subprocess.run("lsb_release -sc", shell=True, capture_output=True, text=True).stdout.strip()
        
        if lsb_release == "noble":
            print("Ubuntu 24.04 (Noble Numbat) detected - using MongoDB's Ubuntu 22.04 (Jammy) repository")
            lsb_release = "jammy" 
            
        print("Removing any existing MongoDB installations...")
        subprocess.run("sudo apt remove --purge mongodb-org* -y", shell=True, check=False)
        subprocess.run("sudo apt autoremove -y", shell=True, check=True)

        print("Adding MongoDB repository...")
        mongo_repo = f"deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu {lsb_release}/mongodb-org/6.0 multiverse"
        subprocess.run(f"echo '{mongo_repo}' | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list", shell=True, check=True)

        print("Importing MongoDB GPG key...")
        subprocess.run("wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo gpg --dearmor -o /usr/share/keyrings/mongodb.gpg", shell=True, check=True)
        
        subprocess.run(f"echo 'deb [ signed-by=/usr/share/keyrings/mongodb.gpg arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu {lsb_release}/mongodb-org/6.0 multiverse' | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list", shell=True, check=True)

        print("Updating APT package list...")
        subprocess.run("sudo apt update", shell=True, check=True)

        print("Installing MongoDB...")
        subprocess.run("sudo apt install -y mongodb-org", shell=True, check=True)

        print("Starting MongoDB...")
        subprocess.run("sudo systemctl start mongod", shell=True, check=True)
        subprocess.run("sudo systemctl enable mongod", shell=True, check=True)

        print("MongoDB installation completed.")
    except subprocess.CalledProcessError as e:
        print(f"Error during MongoDB installation: {e}")
        print("If you're using Ubuntu 24.04, MongoDB might not have official support yet.")
    except Exception as e:
        print(f"Unexpected error during MongoDB installation: {e}")


# Software list with installation commands
softwareList = {
    "Visual Code": {"method": "snap", "command": "sudo snap install code --classic"},
    "GIMP": {"method": "apt", "command": "sudo apt install gimp -y"},
    "Blender": {"method": "apt", "command": "sudo apt install blender -y"},
    "OBS": {"method": "apt", "command": "sudo apt install obs-studio -y"},
    "Gnome Tweaks": {"method": "apt", "command": "sudo apt install gnome-tweaks -y"},
    "VLC": {"method": "apt", "command": "sudo apt install vlc -y"},
    "Node JS": {"method": "apt", "command": "sudo apt install nodejs -y"},
    "Mongo DB Server": {"method": "custom", "command": installMongo},
    "Mongo DB Compass": {"method": "custom", "command": "echo 'i cannot do that sorry'"},
    "Figma": {"method": "snap", "command": "sudo snap install figma-linux"},
    "Enpass": {"method": "snap", "command": "sudo snap install enpass"},
    "Chromium": {"method": "apt", "command": "sudo apt install chromium-browser -y"},
    "Inkscape": {"method": "apt", "command": "sudo apt install inkscape -y"},
    "X-Mind": {"method": "snap", "command": "sudo snap install xmind"},
    "Discord": {"method": "snap", "command": "sudo snap install discord"},
    "CIFS": {"method": "apt", "command": "sudo apt install cifs-utils -y"},
    "Wine": {"method": "apt", "command": "sudo apt install wine64 -y"},
    "Zoom": {"method": "snap", "command": "sudo snap install zoom-client"},
    "Git": {"method": "apt", "command": "sudo apt install git -y"},
    "Putty": {"method": "apt", "command": "sudo apt install putty -y"},
    "Curl": {"method": "apt", "command": "sudo apt install curl -y"},
    "Docker": {"method": "apt", "command": "sudo apt install docker.io -y"},
    "Postgresql": {"method": "apt", "command": "sudo apt install postgresql -y"},
    "Golang": {"method": "apt", "command": "sudo apt install golang -y"},
    "Spotify": {"method": "snap", "command": "sudo snap install spotify"},
    "Postman": {"method": "snap", "command": "sudo snap install postman"}
}

def runCommand(command):
    try:
        if callable(command):
            command() 
        else:
            print(f"Running: {command}")
            subprocess.run(command, shell=True, check=True)
        print("Installation successful!")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def installSoftware(softwareChoice): # installs the chosen software
    software = softwareList.get(softwareChoice)
    if software:
        print(f"Installing {softwareChoice}...")
        runCommand(software["command"])
    else:
        print(f"{softwareChoice} is not a valid choice.")

def Main():# 
    while True:
        print("\nAvailable Software:")
        for idx, software in enumerate(softwareList.keys(), 1):
            print(f"{idx}. {software}")
        print(f"{len(softwareList) + 1}. Install All")
        print(f"{len(softwareList) + 2}. Quit")

        try:
            choice = int(input("\nEnter the number of the software to install or 28 to exit: "))

            if choice == len(softwareList) + 1:
                # Install all software
                for software in softwareList.keys():
                    installSoftware(software)
            elif choice == len(softwareList) + 2:
                print("Exiting the script.")
                break
            elif 1 <= choice <= len(softwareList):
                software_choice = list(softwareList.keys())[choice - 1]
                installSoftware(software_choice)
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

    Main()