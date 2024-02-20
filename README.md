# ServerlessInfrastructure

qemu-system-aarch64 -accel hvf -cpu cortex-a57 -M virt,highmem=off -m 1024 -smp 2  -drive file=/opt/homebrew/Cellar/qemu/8.2.1/share/qemu/edk2-aarch64-code.fd,if=pflash,format=raw,readonly=on  -drive if=none,file=myqcow2image.qcow2,format=qcow2,id=hd0  -device virtio-blk-device,drive=hd0,serial="dummyserial"  -device virtio-net-device,netdev=net0 -netdev user,id=net0,hostfwd=tcp::2222-:22 -vga none -device ramfb -device usb-ehci -device usb-kbd -device usb-mouse -usb  -nographic

在 QEMU 初始化命令中，您已经使用该-netdev user,hostfwd=tcp::2222-:22选项为 SSH（端口 22）配置了端口转发。您可以添加类似的选项来转发端口 8080，这是访问 OpenFaaS UI 的默认端口。



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
    
curl -sSL https://cli.openfaas.com | sudo sh

In order to install faasd on your Linux VM, you can simply run the following commands.
$ git clone https://github.com/openfaas/faasd --depth=1 $ cd faasd
# Install faasd
$ ./hack/install.sh

After the installation, you must obtain your username and password by running
$ sudo cat /var/lib/faasd/secrets/basic-auth-password 
6ITqc92MCGS1ZTtNMaTdMilOq1NYIQDfO5eZf4alIAD3ULuvyWrmUPpfHGqt2u7abiqemu@abimac:~/faasd$ 

Username:admin
password:6ITqc92MCGS1ZTtNMaTdMilOq1NYIQDfO5eZf4alIAD3ULuvyWrmUPpfHGqt2u7

$ sudo cat /var/lib/faasd/secrets/basic-auth-user
adminabiqemu@abimac:~/faasd$ 

You can use this information to log in to the OpenFaaS UI or pass the information to the faas-cli by running the following command. You should be able to use faas-cli after this.

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




