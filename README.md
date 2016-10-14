# AUTOMATIC FIESTA!

Because manually distributing code is annoying.

Version: Beta 1

## Basic usage
First, setup your Automatic Fiesta Server.

1. Clone the repository to what ever you want to be the server. I personally use a Raspberry Pi.
2. Edit "names.json" to have the MAC addresses and names of your nodes. Then decided what file you want to be that node's "main" and what other files you want to be transfered as other assets, be they code or a favicon.
3. run the server script "python server.py"

Second, your nodes:
Connect to your ESP8266 micropython board. Press "Ctrl-E" to go in to paste mode. Paste the contents of "boot.py" into the terminal and Press "Ctrl-D" to run. Right now the boot script has grown to be a little long. So you may need to do the v = "script" first then the file writing second. 

You have just installed the Automatic Fiesta boot script. This script will run when your node reboots and contact your Automatic Fiesta Server and pull down chips, salsa, and this node's Main.py. So restart your node and watch the code come flying in!

## Adanced super cool fun usage!
Automatic Fiesta isn't just a system for distributing code, it also has basic other features you would want to program your nodes. Specifically a simple web server and a simple telnet server. Their usage goes something like this. Say you wanted to have your node blink a light on command:

```python
def blink(val,server=None):
	from machine import Pin
	import time
	p = Pin(2,Pin.OUT)
	p.high()
	time.sleep(1)
	p.low()
	return "I blinked\n"
```

If you wanted to do it via a telnet server it would work like this:

```python
from TelnetFiesta import *
telserver = TelnetServer()
telserver.registerFunction("blink",blink)
telserver.run()
```

Similiarly for a web server it would work like this:

```python
from WebFiesta import *
webserver = WebFiesta()
webserver.registerFunction("blink",blink)
webserver.run()
```

That's it! you now have a web-enabled blink! I personally recommend you now install "Automate" by llamalab on your android phone and use it to make buttons on your home screen to call the node. I use it for my garage door and my kitchen lights. Super simple. 

## Call for help!
"premature optimization is the root of all evil." - Donald Knuth
So I've got this system up and running, but it is far from perfect, this is certainly a early beta at this point. Right now the biggest problem is much of this system takes up to much RAM on the ESP. So please, make improvements, submit some pull requests!

## Road map:

Features Working:
* Basic server to that responds and gives out code.
* boot.py script that pulls down code and saves it to main.py
* Master getting the normal MAC address out of the ESP8266 MicroPython instance.
* Have the ability for multiple files to be transfered.
* Add default methods to the Automatic-Fiesta server for basic maintenance. Most noteably, reboot. This is done through telnet.
* Create a simple default server that can take the user's command and wrap it up nicely.

Features to work on:
* Have the server warn that the total size of the script(s) to be transfered is bigger than what some or all ESP boards can handle.

NB: The Fructose example currently uses a feature that isn't in the master branch of micropython. I'd advise avoid it for now. 

