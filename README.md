# light-to-sound
a set of scripts that will read input from a camera and create sounds from it

1. Download the raspberry pi desktop and Raspberry Pi Imager https://www.raspberrypi.com/software/
2. Use the Raspberry Pi Imager to install the OS to your micro SD card and configure WiFi and users
3. Once the RPi is up and running, install the following packages:
   sudo apt install fswebcam
   sudo apt install motion
4. Use the "check-output.py" python script to find out which audio source is being used.
5. edit "sounds.py" to add the output_device_index=<output id>
