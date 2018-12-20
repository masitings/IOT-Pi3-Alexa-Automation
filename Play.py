""" name_port_gpio.py
 
    This is a demo python file showing how to take paramaters
    from command line for device name, port, and GPIO.
    All credit goes to https://github.com/toddmedema/echo/
    for making the first working versions of this code.
"""
 
import fauxmo
import logging
import time
import sys
import RPi.GPIO as GPIO ## Import GPIO library
 
from debounce_handler import debounce_handler
 
logging.basicConfig(level=logging.DEBUG)
 
class device_handler(debounce_handler):
    """Publishes the on/off state requested,
       and the IP address of the Echo making the request.
    """
    #TRIGGERS = {str(sys.argv[1]): int(sys.argv[2])}
    #TRIGGERS = {"office": 52000}
    TRIGGERS = {"socket 1": 52000,"socket 2":51000}

    def act(self, client_address, state, name):
        print("State", state, "from client @", client_address)
        if name=="socket 1":
            GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
            GPIO.setup(int(35), GPIO.OUT)   ## Setup GPIO Pin to OUTPUT
            GPIO.output(int(35), state) ## State is true/false
        elif name =="socket 2":
            GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
            GPIO.setup(int(37), GPIO.OUT)   ## Setup GPIO Pin to OUTPUT
            GPIO.output(int(37), state) ## State is true/false
        elif name =="flash room":
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(int(40), GPIO.OUT)
            GPIO.output(int(40), state)
        else:
            print("Device not found!")




        return True
 
if __name__ == "__main__":
    # Startup the fauxmo server
    fauxmo.DEBUG = True
    p = fauxmo.poller()
    u = fauxmo.upnp_broadcast_responder()
    u.init_socket()
    p.add(u)
 
    # Register the device callback as a fauxmo handler
    d = device_handler()
    for trig, port in d.TRIGGERS.items():
        fauxmo.fauxmo(trig, u, p, None, port, d)
 
    # Loop and poll for incoming Echo requests
    logging.debug("Entering fauxmo polling loop")
    while True:
        try:
            # Allow time for a ctrl-c to stop the process
            p.poll(100)
            time.sleep(0.1)
        except Exception as e:
            logging.critical("Critical exception: "+ e.args  )
            break
