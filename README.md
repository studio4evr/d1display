A low cost display system for a synced slidehow on 9 HDMI outputs, with a stylised transition between each slide.

Using 5x networked Pi4 B with 4Gb ram and preinstalled 32gb Pi OS.

Run server.py on Pi 001, with clientWithFeh.py running on Pi 002, Pi 003 and Pi 004. If you need the last display to run a single display make sure to use client5.py

System has potential to be scaled to 2 more screens per Pi added to cluster.

Install libraries and add respective scripts to autostart at:

nano ~/.config/lxsession/LXDE-pi/autostart

change static IP of each client Pi at
nano /etc/network/interfaces

Go into raspi-config and switch the window system from Wayland to X11. (It's possible the X compatibility layer in Wayland ignores the geometry specifiers.)

Put Slides into /Slide folder, run once and wait for one-time compilation of the slideshow.

You may need to adjust some IP variables and timings in code to suit your needs. 

** Assembly ** 

Shopping List:

HDMI couplers

Case

PSU

HDMI mounts

5x USB solderable power cords: 
Xiatiaosann USB C Connector DIY Solderable 2 Wire Power Supply Extension Cable Charger Connector Plug 2 Pin Line for PCB USB to DIP Adapter for Arduino, LED Strips, 4 PCS USB Male + 4 PCS USB Female : Amazon.co.uk: Computers & Accessories

Pi Rack

Network Switch: TP-Link TL-SG105S, 5 Port Gigabit Ethernet Network Switch, Ethernet Splitter, Hub, Desktop and Wall-Mounting, Sturdy Metal, Fanless, Plug and Play, Energy-Saving : Amazon.co.uk: Computers & Accessories

Ethernet Leads (5x 0.3m): Pro Signal PSG03119 Cat5e RJ45 Ethernet Patch Lead, 0.3m Black : Amazon.co.uk: Computers & Accessories

5x sandisk 32gb class 10 a1 micro sd cards: SanDisk Ultra 32 GB microSDHC Memory Card + SD Adapter with A1 App Performance Up to 120 MB/s, Class 10, U1 (Twin Pack) : Amazon.co.uk: Computers & Accessories

5 x Pi 4 Bs 4gb ram Raspberry Pi 4 Model B | The Pi Hut

Fan: BQLZR 5V Black 8CM 8025 USB Silent Power Ball Bearing Computer Case Cooling Fan for Computer Case CPU Cooler : Amazon.co.uk: Computers & Accessories

Notes:

Drill holes in the case for fixing fan, HDMI mounts, PSU and cluster.

Assemble giving care to soldering 5V power inputs on the Pis, fan and Network switch to 5v power outputs on the Case. If in doubt, consult an electrical engineer.

	



