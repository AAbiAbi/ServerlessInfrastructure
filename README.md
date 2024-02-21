# ServerlessInfrastructure
```bash
qemu-system-aarch64 -accel hvf -cpu cortex-a57 -M virt,highmem=off -m 1024 -smp 2  -drive file=/opt/homebrew/Cellar/qemu/8.2.1/share/qemu/edk2-aarch64-code.fd,if=pflash,format=raw,readonly=on  -drive if=none,file=myqcow2image.qcow2,format=qcow2,id=hd0  -device virtio-blk-device,drive=hd0,serial="dummyserial"  -device virtio-net-device,netdev=net0 -netdev user,id=net0,hostfwd=tcp::2222-:22 -vga none -device ramfb -device usb-ehci -device usb-kbd -device usb-mouse -usb  -nographic
```

在 QEMU 初始化命令中，您已经使用该-netdev user,hostfwd=tcp::2222-:22选项为 SSH（端口 22）配置了端口转发。您可以添加类似的选项来转发端口 8080，这是访问 OpenFaaS UI 的默认端口。


```bash
qemu-system-aarch64 \
    -accel hvf \
    -cpu cortex-a57 \
    -M virt,highmem=off \
    -m 1024 \
    -smp 2 \
    -drive file=/opt/homebrew/Cellar/qemu/8.2.1/share/qemu/edk2-aarch64-code.fd,if=pflash,format=raw,readonly=on \
    -drive if=none,file=myqcow2image.qcow2,format=qcow2,id=hd0 \
    -device virtio-blk-device,drive=hd0,serial="dummyserial" \
    -device virtio-net-device,netdev=net0 \
    -netdev user,id=net0,hostfwd=tcp::2222-:22,hostfwd=tcp::8080-:8080 \
    -vga none \
    -device ramfb \
    -device usb-ehci \
    -device usb-kbd \
    -device usb-mouse \
    -usb \
    -nographic
```
```bash
curl -sSL https://cli.openfaas.com | sudo sh
```

In order to install faasd on your Linux VM, you can simply run the following commands.
```bash
$ git clone https://github.com/openfaas/faasd --depth=1 $ cd faasd
```
```bash
# Install faasd
$ ./hack/install.sh
```

After the installation, you must obtain your username and password by running
```bash
$ sudo cat /var/lib/faasd/secrets/basic-auth-password 
6ITqc92MCGS1ZTtNMaTdMilOq1NYIQDfO5eZf4alIAD3ULuvyWrmUPpfHGqt2u7abiqemu@abimac:~/faasd$
```

Username:admin
password:6ITqc92MCGS1ZTtNMaTdMilOq1NYIQDfO5eZf4alIAD3ULuvyWrmUPpfHGqt2u7


``` bash
$ sudo cat /var/lib/faasd/secrets/basic-auth-user
adminabiqemu@abimac:~/faasd$ 
```
You can use this information to log in to the OpenFaaS UI or pass the information to the faas-cli by running the following command. You should be able to use faas-cli after this.
```bash
sudo systemctl status faasd
● faasd.service - faasd
     Loaded: loaded (/lib/systemd/system/faasd.service; enabled; vendor preset:>
     Active: active (running) since Tue 2024-02-20 06:06:19 UTC; 11min ago
   Main PID: 638 (faasd)
      Tasks: 7 (limit: 1015)
     Memory: 28.2M (limit: 500.0M)
     CGroup: /system.slice/faasd.service
             └─638 /usr/local/bin/faasd up

Feb 20 06:06:21 abimac faasd[638]: 2024/02/20 06:06:21 Resolver: "localhost"="1>
Feb 20 06:06:21 abimac faasd[638]: 2024/02/20 06:06:21 Resolver: "faasd-provide>
Feb 20 06:06:21 abimac faasd[638]: 2024/02/20 06:06:21 Resolver: "nats"="10.62.>
Feb 20 06:06:21 abimac faasd[638]: 2024/02/20 06:06:21 Resolver: "queue-worker">
Feb 20 06:06:21 abimac faasd[638]: 2024/02/20 06:06:21 Resolver: "prometheus"=">
Feb 20 06:06:21 abimac faasd[638]: 2024/02/20 06:06:21 Resolver: "gateway"="10.>
Feb 20 06:06:21 abimac faasd[638]: 2024/02/20 06:06:21 Looking up IP for: "prom>
Feb 20 06:06:21 abimac faasd[638]: 2024/02/20 06:06:21 Proxy from: 127.0.0.1:90>
Feb 20 06:06:21 abimac faasd[638]: 2024/02/20 06:06:21 faasd: waiting for SIGTE>
Feb 20 06:06:21 abimac faasd[638]: 2024/02/20 06:06:21 Proxy from: 0.0.0.0:8080>
lines 1-19/19 (END)
```
```bash
sudo cat /var/lib/faasd/secrets/basic-auth-password | faas-cli login --username admin --password-stdin


abiqemu@abimac:~$ sudo systemctl status faasd-provider
● faasd-provider.service - faasd-provider
     Loaded: loaded (/lib/systemd/system/faasd-provider.service; enabled; vendo>
     Active: active (running) since Tue 2024-02-20 06:06:19 UTC; 12min ago
   Main PID: 636 (faasd)
      Tasks: 5 (limit: 1015)
     Memory: 16.6M (limit: 500.0M)
     CGroup: /system.slice/faasd-provider.service
             └─636 /usr/local/bin/faasd provider

Feb 20 06:06:19 abimac systemd[1]: Started faasd-provider.
Feb 20 06:06:19 abimac faasd[636]: 2024/02/20 06:06:19 faasd-provider starting.>
Feb 20 06:06:19 abimac faasd[636]: faasd version: 0.18.6        commit: c61efe0>
Feb 20 06:06:19 abimac faasd[636]: 2024/02/20 06:06:19 Writing network config...
Feb 20 06:06:19 abimac faasd[636]: 2024/02/20 06:06:19 Listening on: 0.0.0.0:80>
lines 1-14/14 (END)
```

```bash

abiqemu@abimac:~$ faas-cli store list

FUNCTION          AUTHOR       DESCRIPTION
nodeinfo          openfaas     NodeInfo
env               openfaas     env
sleep             openfaas     sleep
shasum            openfaas     shasum
figlet            openfaas     figlet
printer           openfaas     printer
curl              openfaas     curl
external-ip       openfaas     external-ip
youtube-dl        openfaas     youtube-dl
sentimentanalysis openfaas     SentimentAnalysis
hey               openfaas     hey
nslookup          openfaas     nslookup
certinfo          stefanprodan SSL/TLS cert info
alpine            openfaas     alpine
cows              openfaas     ASCII Cows
```
```bash
# Deploy figlet
abiqemu@abimac:~$ faas-cli store deploy figlet


Deployed. 200 OK.
URL: http://127.0.0.1:8080/function/figlet

# Find the URLs for the function

abiqemu@abimac:~$ faas-cli store inspect figlet
Title:       figlet
Author:      openfaas
Description: 
Generate ASCII logos with the figlet CLI

Image:    ghcr.io/openfaas/figlet:latest
Process:  figlet
Repo URL: https://github.com/openfaas/store-functions

# Create some ASCII

abiqemu@abimac:~$ echo "Hello, FaaS, world" | faas-cli invoke figlet
 _   _      _ _          _____           ____                        _     _ 
| | | | ___| | | ___    |  ___|_ _  __ _/ ___|   __      _____  _ __| | __| |
| |_| |/ _ \ | |/ _ \   | |_ / _` |/ _` \___ \   \ \ /\ / / _ \| '__| |/ _` |
|  _  |  __/ | | (_) |  |  _| (_| | (_| |___) |   \ V  V / (_) | |  | | (_| |
|_| |_|\___|_|_|\___( ) |_|  \__,_|\__,_|____( )   \_/\_/ \___/|_|  |_|\__,_|
                    |/                       |/                              
abiqemu@abimac:~$ echo "Hello, FaaS, world,this is Ningchen" | faas-cli invoke figlet
 _   _      _ _          _____           ____   
| | | | ___| | | ___    |  ___|_ _  __ _/ ___|  
| |_| |/ _ \ | |/ _ \   | |_ / _` |/ _` \___ \  
|  _  |  __/ | | (_) |  |  _| (_| | (_| |___) | 
|_| |_|\___|_|_|\___( ) |_|  \__,_|\__,_|____( )
                    |/                       |/ 
                    _     _  _   _     _       _     
__      _____  _ __| | __| || |_| |__ (_)___  (_)___ 
\ \ /\ / / _ \| '__| |/ _` || __| '_ \| / __| | / __|
 \ V  V / (_) | |  | | (_| || |_| | | | \__ \ | \__ \
  \_/\_/ \___/|_|  |_|\__,_( )__|_| |_|_|___/ |_|___/
                           |/                        
 _   _ _                  _                
| \ | (_)_ __   __ _  ___| |__   ___ _ __  
|  \| | | '_ \ / _` |/ __| '_ \ / _ \ '_ \ 
| |\  | | | | | (_| | (__| | | |  __/ | | |
|_| \_|_|_| |_|\__, |\___|_| |_|\___|_| |_|

               |___/                       
```
Step 5: Signing Up for DockerHub
In order for you to be able to push your function to the public, you would need a Docker hub account. Please sign up for one at https://hub.docker.com/ if you don’t have one. Make sure you note down your Docker Hub account and the password to be used in the next step.

Note Your Credentials:

Write down your Docker Hub username and password, or use a password manager. You'll need them to log in to Docker Hub from the command line.
Login from Command Line:

Once you have your Docker Hub account, you will need to log in from your local machine using the Docker CLI. This is usually done with the following command:
bash
Copy code
docker login
When prompted, enter your Docker Hub username and password.
Push Your Function's Image:

After logging in, you can push your Docker images to Docker Hub. Typically, you'd build your Docker image with a tag that includes your Docker Hub username, like so:
bash
Copy code
docker build -t <your-dockerhub-username>/<repository-name>:<tag> .
Then you'd push the image to Docker Hub:
bash
Copy code
docker push <your-dockerhub-username>/<repository-name>:<tag>
Update Your OpenFaaS Function:

If you're working with OpenFaaS, you'll update your function's definition to use the Docker image from Docker Hub and then deploy it to OpenFaaS.
Remember, your Docker Hub repository is public by default, meaning anyone can pull and use your Docker images. If you want to keep your images private, you can create a private repository on Docker Hub, but note that the free account has a limit on the number of private repositories you can have.

Keep your credentials secure and ensure that you follow best practices for managing Docker images, such as not including sensitive data in your Docker images and using .dockerignore files to prevent unnecessary files from being added to the image.

(base) NLiangs-MacBook-Pro:tmp a25076$ docker login
Login with your Docker ID to push and pull images from Docker Hub. If you don't have a Docker ID, head over to https://hub.docker.com to create one.
Username: abiliang1
Password: 
Login Succeeded



Logging in with your password grants your terminal complete access to your account. 
For better security, log in with a limited-privilege personal access token. Learn more at https://docs.docker.com/go/access-tokens/

Create a Base Folder for Functions:

The first command creates a directory for your OpenFaaS functions:
```bash
mkdir -p ~/functions && cd ~/functions
```
```bash
abiqemu@abimac:~$ mkdir -p ~/functions && cd ~/functions
abiqemu@abimac:~/functions$ 
abiqemu@abimac:~/functions$ ls
abiqemu@abimac:~/functions$ pwd
/home/abiqemu/functions
```
abiqemu@abimac:~/functions$ 

Initialize New Functions with faas-cli:

The faas-cli new command is used to create a new function with a specified language template. In your case, you're using the Python language template.
Running these commands will generate boilerplate code for two functions named slack-request and slack-interactive:

```bash
abiqemu@abimac:~/functions$ faas-cli new --lang python slack-request
2024/02/20 10:29:07 No templates found in current directory.
2024/02/20 10:29:07 Attempting to expand templates from https://github.com/openfaas/templates.git
2024/02/20 10:29:08 Fetched 17 template(s) : [bun csharp dockerfile go java11 java11-vert-x node node14 node16 node17 node18 php7 php8 python python3 python3-debian ruby] from https://github.com/openfaas/templates.git
Folder: slack-request created.
  ___                   _____           ____
 / _ \ _ __   ___ _ __ |  ___|_ _  __ _/ ___|
| | | | '_ \ / _ \ '_ \| |_ / _` |/ _` \___ \
| |_| | |_) |  __/ | | |  _| (_| | (_| |___) |
 \___/| .__/ \___|_| |_|_|  \__,_|\__,_|____/
      |_|


Function created in folder: slack-request
Stack file written: slack-request.yml
```

```bash
abiqemu@abimac:~/functions$ faas-cli new --lang python slack-interactive
Folder: slack-interactive created.
  ___                   _____           ____
 / _ \ _ __   ___ _ __ |  ___|_ _  __ _/ ___|
| | | | '_ \ / _ \ '_ \| |_ / _` |/ _` \___ \
| |_| | |_) |  __/ | | |  _| (_| | (_| |___) |
 \___/| .__/ \___|_| |_|_|  \__,_|\__,_|____/
      |_|


Function created in folder: slack-interactive
Stack file written: slack-interactive.yml
```

Update the Generated Code with Skeleton Code:

After running the faas-cli new commands, you'll have two new directories each containing handler.py, a YAML file (which will be named after your functions, such as slack-request.yml and slack-interactive.yml), and a requirements.txt file.
```bash
abiqemu@abimac:~/functions$ ls
slack-interactive      slack-request      template
slack-interactive.yml  slack-request.yml
abiqemu@abimac:~/functions$ cd slack-interactive/
abiqemu@abimac:~/functions/slack-interactive$ ls
handler.py  requirements.txt
```
Replace the contents of handler.py and the YAML files with the skeleton code you've been provided and fill in the blanks as required.
Make sure to also add any Python dependencies your functions might need into requirements.txt.

Log in to Docker:

Before you can push your Docker images to Docker Hub, you need to log in. This is done using:
```bash

docker login
```
Enter your Docker Hub username and password when prompted.
Build, Push, and Deploy Functions:

Use faas-cli build to build Docker images for your functions based on the YAML files.
Use faas-cli push to push the built images to Docker Hub.
Use faas-cli deploy to deploy your functions to your OpenFaaS cluster.
The commands are as follows:
```bash

faas-cli build -f ./slack-interactive.yml
faas-cli push -f ./slack-interactive.yml
faas-cli deploy -f ./slack-interactive.yml

faas-cli build -f ./slack-request.yml
faas-cli push -f ./slack-request.yml
faas-cli deploy -f ./slack-request.yml
```
It's important that your YAML files contain the correct Docker image names, which should follow the format <your-dockerhub-username>/<repository-name>:<tag>.
Note: You might need to run some of these commands with sudo, depending on your setup.

After these steps, your functions should be built, pushed to Docker Hub, and deployed to OpenFaaS, making them callable via the gateway. Remember to test your functions to make sure they work as expected before considering the deployment complete.

Creating a chatbot as a serverless function involves setting up a function that can receive input, process it according to specific rules, and return a response. Here's how you could approach writing a chatbot function with the requirements you've described:

Set up the Function: Similar to Step 6, use the faas-cli new command to create a new function template. You might want to use a Python template if you're comfortable with Python, or choose another supported language you're familiar with.

Implement the Logic:

User Input: Your function should be designed to accept a string as user input.
Response Logic: Write logic within your handler function to handle different types of questions:
Name: If the input matches questions about the chatbot's name, return one of three predetermined responses.
Current Date and Time: If the input is about the current date or time, use a library or the language's built-in functionality to get the current date and time and return it in the response.
Figlet Generation: If the input is a request to generate a figlet, your function should call the previously deployed figlet function and return its output.
Here's a high-level example in Python for the chatbot function logic (to be put in handler.py):

```python
import datetime
import subprocess

def handle(req):
    # Case for asking the bot's name
    if "name" in req.lower():
        return "My name is Chatbot. You can call me 'Bot' or simply 'Chatbot'."

    # Case for asking the current time
    elif "current time" in req.lower() or "date" in req.lower():
        now = datetime.datetime.now()
        return f"The current time is {now.strftime('%H:%M:%S')} and today's date is {now.strftime('%Y-%m-%d')}."

    # Case for generating a figlet
    elif req.lower().startswith("generate a figlet for"):
        figlet_text = req[len("generate a figlet for"):].strip()
        # Invoke the figlet function using faas-cli
        result = subprocess.run(["faas-cli", "invoke", "figlet"], input=figlet_text, capture_output=True, text=True)
        return result.stdout

    # Default case if none of the above questions are asked
    else:
        return "I am not sure how to answer that. Can you ask something else?"

# Replace subprocess.run(...) with the appropriate way to invoke another function in your environment
```

Handle Dependencies:

Make sure to include any dependencies in the requirements.txt if you are using Python or the equivalent for other languages.
Deploy the Function:

Use faas-cli build, faas-cli push, and faas-cli deploy commands to build, push, and deploy your chatbot function.
Test Your Function:

Ensure that you test your function extensively. You can do this by invoking the function with different inputs to see if you get the expected outputs.
Once you have completed the implementation and deployment, you will be ready to answer questions about how you designed and implemented the chatbot, its capabilities, and any challenges you faced.






