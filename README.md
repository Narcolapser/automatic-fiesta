# AUTOMATIC FIESTA!

Because manually distributing code is annoying.

## Basic usage
First, setup your Automatic Fiesta Server.
1. Clone the repository to what ever you want to be the server. I personally use a Raspberry Pi.
2. Edit "names.json" to have the MAC addresses and names of your nodes. Then decided what file you want to be that node's "main" and what other files you want to be transfered as other assets, be they code or a favicon.
3. run the server script "python server.py"

Second, your nodes:
Connect to your ESP8266 micropython board. Press "Ctrl-E" to go in to paste mode. Paste the contents of "boot.py" into the terminal and Press "Ctrl-D" to run. Right now the boot script has grown to be a little long. So you may need to do the v = "script" first then the file writing second. 

You have just installed the Automatic Fiesta boot script. This script will run when your node reboots and contact your Automatic Fiesta Server and pull down chips, salsa, and this node's Main.py. So restart your node and watch the code come flying in!

Now, the second part of this is simplification of the process of creating systems. I'll write more on this tomorrow, right now my wife is telling me it's bed time.


NB: The Fructose example currently uses a feature that isn't in the master branch of micropython. I'd advise avoid it for now. 

## Road map:

Features Working:
* Basic server to that responds and gives out code.
* boot.py script that pulls down code and saves it to main.py
* Master getting the normal MAC address out of the ESP8266 MicroPython instance.
* Have the ability for multiple files to be transfered.
* Add default methods to the Automatic-Fiesta server for basic maintenance. Most noteably, reboot. This is done through telnet.
* Create a simple default server that can take the user's command and wrap it up nicely. So if you want to make a blink it works like:

Features to work on:
* Have the server warn that the total size of the script(s) to be transfered is bigger than what some or all ESP boards can handle.
