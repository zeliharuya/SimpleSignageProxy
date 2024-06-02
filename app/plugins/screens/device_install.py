import json
import os
import requests
import re


#todo input sanitization

def read(id=False): # GET
    if id == False or id == "":
        return {"text": "This is the Device onboarding script that you can run on e.g. a raspberry pi. <br> Nothing else to do here. <br><br><a id=\"device_install_url\" target=\"_blank\" href=\"/plugins/screens/device_install?id=\">Open Bash Install Script</a><script>document.getElementById(\"device_install_url\").href += window.location.hostname</script>"}
    else:
        script="""
apt install unclutter xdotool

mkdir -p /etc/chromium/policies/managed /etc/chromium/policies/recommended
mkdir -p /home/pi/.config/lxsession/LXDE-pi/


echo -ne '{{\\n"HomepageLocation":"http://'$(hostname -s)'.{0}",\\n"NewTabPageLocation":"http://'$(hostname -s)'.{0}",\\n"ShowHomeButton":true,\\n"RestoreOnStartup":5}}'>/etc/chromium/policies/managed/CHROME-GLOBAL.json

cat > /home/pi/refresh.sh <<'EOL'
#!/bin/bash
export XAUTHORITY=/home/pi/.Xauthority
export DISPLAY=:0
#xdotool search --onlyvisible --class chromium windowfocus key F5
xdotool search --onlyvisible --class chromium windowfocus key ctrl+t
sleep 2
xdotool search --onlyvisible --class chromium windowfocus key ctrl+Tab
sleep 30
xdotool search --onlyvisible --class chromium windowfocus key ctrl+w
EOL

chmod +x /home/pi/refresh.sh
echo -ne "dtoverlay=disable-bt\\ndtoverlay=disable-wifi\\navoid_warnings=1\\n" >> /boot/config.txt

echo -ne "*/15 * * * * /home/pi/refresh.sh >/dev/null 2>&1\\n" > mycron
crontab -u pi mycron
echo -ne "@reboot dmesg -n 1\\n0 0 * * * reboot\\n" > mycron
crontab -u root mycron
rm mycron


cat > /home/pi/.config/lxsession/LXDE-pi/autostart <<EOL

# Bildschirmschoner deaktivieren
@xset s off
@xset -dpms
@xset s noblank

# Chromium automatisch im incognito- und Kiosk-Modus starten und eine Seite öffnen
@chromium-browser --kiosk http://$(hostname -s).{0} --kiosk --noerrdialogs --disable-infobars --no-first-run --enable-features=OverlayScrollbar --start-maximized --ignore-certificate-errors
#switchtab = bash ~/switchtab.sh

# Mauszeiger deaktivieren
@unclutter

EOL

        """.format(id)
        return script
