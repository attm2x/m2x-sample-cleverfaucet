# Sample Smart Faucet using AT&T's M2X and Raspberry Pi
<img align="left" src="/logo.png"> This Python app for your Raspberry Pi records how much water and what temperature water is being used at a faucet connected to your Pi using a flowmeter and a temperature sensor. It then will send that information to AT&T's [M2X](https://m2x.att.com) service where it is stored for future retrieval and analysis.

If you want to display the data from your faucet, here’s a quick app that you can deploy to Heroku: https://github.com/attm2x/m2x-sample-cleverfaucet-web

## What you need
* Familiarity with the AT&T [M2X API](https://m2x.att.com/developer/documentation/v2/overview)
* Raspberry Pi running [RaspBian](http://www.raspbian.org)
* A free AT&T [M2X Account](https://m2x.att.com/signup).
* Suggested Sensors:
    * [DS18B20 Digital temperature sensor](http://www.adafruit.com/products/381) - _If using a different one, make sure it is waterproof_
    * [Liquid Flow Meter - Plastic 1/2" NPS Threaded](http://www.adafruit.com/product/828)
* 4.7k Ohm resistor, jumper wires, and a breadboard 

## Dependencies

* Python running on your Raspberry Pi ([Tutorial](https://m2x.att.com/developer/tutorials/raspberry))
* [m2x-python](https://github.com/attm2x/m2x-python) - v3.0.4
* [RPi.GPIO](https://pypi.python.org/pypi/RPi.GPIO) - _If you are running Raspbian this should already be included with its Python installation_ 

## Instructions
1. Clone this repository
 
  ```bash
  $ git clone https://github.com/attm2x/m2x-sample-cleverfaucet
  $ cd faucet
  ```

2. [Create a new M2X device](https://m2x.att.com/devices?).
3. Copy the Device ID from the device page.
4. From your [M2X account page](https://m2x.att.com/account#master-keys) get your Master API Key.
5. Create two data streams in that device. One named 'water_use' and the other named 'temperature'.
6. In main.py replace MASTER_API_KEY and DEVICE_ID:
 ```python
client = M2XClient(MASTER_API_KEY)
device = client.devices.get(DEVICE_ID)
```
    with:
 ```python
client = M2XClient('your_key_here')
device = client.devices.get('device_id_here')
```

7. **WARNING: Wiring this incorrectly could fry your Pi so proceed with caution.**

    Use the following diagram to connect the sensors to your pi: ![Wiring diagram](http://i.imgur.com/fOHUP1D.png "Logo Title Text 1")

    Here is the GPIO Diagram from the various Pi Models:
    ![](http://raspi.tv/wp-content/uploads/2014/07/Raspberry-Pi-GPIO-pinouts.png)
8. Place the faucet directory on your Pi. Now simply run the following:
  ```bash
  $ sudo ./start.sh
  ```

9. Check out the data streams on M2X and you should see them update when you use the faucet! 

##LICENSE

This sample application is released under the MIT license. See [`LICENSE`](LICENSE) for the terms.

