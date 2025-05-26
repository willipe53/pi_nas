# DON'T RUN THIS FILE
# DOCUMENTATION PURPOSES ONLY
exit 1

sudo raspi-config
sudo lsblk
sudo dd if=/dev/zero of=/dev/sda bs=512 count=10000
sudo parted /dev/sda mklabel gpt
sudo parted /dev/sda -a opt mkpart primary 0% 100%
sudo mkfs.ext4 -L backups /dev/sda1
sudo mkdir /mnt/backups
sudo mount /mnt/backups
systemctl daemon-reload
sudo apt install hdparm -y
sudo hdparm -S 120 /dev/disk/by-label/backups
sudo adduser --disabled-password --gecos "" keeper
sudo chown -R keeper: /mnt/backups
sudo apt install samba avahi-daemon -y
sudo vi /etc/samba/smb.conf 
sudo smbpasswd -a keeper
sudo service smbd reload
sudo vi /etc/avahi/services/samba.service
sudo service avahi-daemon restart
sudo apt update
sudo apt install -y i2c-tools
i2cdetect -y 1
pip install adafruit-circuitpython-ssd1306
