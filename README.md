# AUTOMATIC FIESTA!

Because manually distributing code is annoying.

## Basic usage
First, setup your Automatic Fiesta Server.
1. Clone the repository to what ever you want to be the server. I personally use a Raspberry Pi.
2. Edit "names.json" to have the MAC addresses and names of your nodes. The name you give your node will be the name of the file you will be sending to your node.
3. run the server script "python server.py"

Second, your nodes:
Connect to your ESP8266 micropython board. Press "Ctrl-E" to go in to paste mode. Paste the contents of "boot.py" into the terminal and Press "Ctrl-D" to run.

### IMPORTANT NOTE
I haven't mastered getting MAC addresses from the nodes programatically. So on line 22 of boot.py you will need to replace the mac address with what ever your current Node's MAC address is. Or just some other string to identify it. Right now it doesn't matter, when I've got MAC address being pulled in automatically, then it will matter.
### BACK TO COOL STUFF

You have just installed the Automatic Fiesta boot script. This script will run when your node reboots and contact your Automatic Fiesta Server and pull down chips, salsa, and this node's Main.py. So restart your node and watch the code come flying in!

This whole system is still very new. So far it represents one evening of fiddling. But hopefully it will be an awesome system for allowing us to be maximum lazy soon!

NB: The Fructose example currently uses a feature that isn't in the master branch of micropython. I'd advise avoid it for now. 

## Road map:

Features Working:
* Basic server to that responds and gives out code.
* boot.py script that pulls down code and saves it to main.py
* Master getting the normal MAC address out of the ESP8266 MicroPython instance.
* Have the ability for multiple files to be transfered.
* Add default methods to the Automatic-Fiesta server for basic maintenance. Most noteably, reboot. This is done through telnet.

Features to work on:
* Have the server warn that the total size of the script(s) to be transfered is bigger than what some or all ESP boards can handle.
* Create a simple default server that can take the user's command and wrap it up nicely. So if you want to make a blink it works like:
```
    import Automatic-Fiesta
    def blink():
        pin.high()
        pin.low()
    af = Automatic-Fiesta(command=blink,port=8080)
    af.run()
    #now if you go to 192.esp.82.66:8080/blink it calls the blink function! easy!
```
