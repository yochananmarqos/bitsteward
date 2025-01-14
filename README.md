# Bitsteward
## If you want to try out Bitsteward, it is highly recommended that you use a vault with data that you do not mind being considered leaked. The current implementation is *not* secure, and any program could potentially see all your vault items. (The screenshots are from a Bitwarden vault created specifically for the development of this application)

Bitsteward is a very early alpha Bitwarden client made with GTK4 and Libadwaita. It is NOT secure at the moment

🚧 The readme is under construction! 🚧

## How to run
The first step is to clone the repo in a terminal
```bash
git clone https://github.com/Bitsteward/bitsteward.git
cd bitsteward
```
Then, you need to login to a Bitwarden account (I recommend creating a new one to test this app as it is not yet secure)
```bash
chmod +x bw
./bw login
```
Then fill in the steps to login as the prompt tells you.
Then you will need to copy the Session ID that bw gives you when the login is successful.
After that, modify the following command to replace {session id} including the brackets with the copied session ID
```
echo 'BW_SESSION="{session id}"' >> .env
```
<details>
    <summary><b>Here is an example of what the command should look like</b></summary>
    
    echo 'BW_SESSION="vdXQ7mRYtcFXueH/Ml+ZgvK//V+0cTJpuAVddMwttNEvVHU6d6xaaRdYokv/9Jqw1uofMq82/B3y/MpV2Yh3Qg=="' >> .env
</details>

After that is done, install the python dependencies
```
pip install -r requirements.txt
```
The last step is to start the application!
```
python3 src/main.py
```


<details>
    <summary><h2>Screenshots</h2></summary>

<picture>
  <source srcset="/screenshots/full-dark-1.png?raw=true" media="(prefers-color-scheme: dark)">
  <img src="/screenshots/full-light-1.png?raw=true" title="App with two columns" alt="screenshot-desktop">
</picture>
    
<picture>
  <source srcset="/screenshots/mobile-dark-1.png?raw=true" media="(prefers-color-scheme: dark)">
  <img src="/screenshots/mobile-light-1.png?raw=true" title="App with two columns" alt="screenshot-desktop">
</picture>
</details>
