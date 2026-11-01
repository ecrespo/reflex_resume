Title: Installing Asterisk
Date: 2008-04-13 10:00
lang: en
Category: Asterisk, Debian, Linux

For a year now I have been working with Asterisk, and now that 
I have managed to buy a Motorola X100P card, I will be able to create a 
gateway to the public telephone network.

### Installing Asterisk.

To install Asterisk from source you first need to 
install some packages:
```
aptitude install libnewt0.52 libnewt-pic libnewt-dev zlib1g zlib1g-dev dcmtk libdcmtk1 libdcmtk1-dev libssl-dev libssl0.9.8 libssl0.9.8-dbg initramfs-tools libnewt0.52 libnewt-pic libnewt-dev
```
Procedure:
1. Installing zaptel: running lspci shows that the Motorola card 
is installed:
```
01:00.0 Communication controller: Motorola Wildcard X100P
```
1.1. Unpack zaptel
```
tar ­-zxvf zaptel­1.4.9.2.tar.gz
```

1.2. Change to the zaptel directory
```
cd zaptel-1.4.9.2/
```
1.3. Configure zaptel
```
./configure
```

1.4. Run make menuselect
1.5. Run make
1.6. Run make install
1.7. Run make config
1.8. Create the udev file for zaptel
```
make install-udev
```

This will create a daemon that brings up the X100P card automatically.

1.9. Check that zaptel detects the card.
```
zaptel_hardware
pci:0000:01:00.0 wcfxo- 1057:5608 Wildcard X100P
```

1.10. Edit /etc/zaptel.conf and add fxsks=1
1.11. Load the module with /etc/init.d/zaptel restart

2. Installing libpri.
2.1. Unpack libpri
```
tar -xvzf libpri-1.4.3.tar.gz
```
2.2. Change to the directory
```
cd libpri-1.4.3/
```
2.3. Run make
2.4. Run make install
3. Install Asterisk
3.1. Unpack Asterisk
```tar -xvzf asterisk-1.4.19.tar.gz
```
3.2. Change to the directory
```
cd asterisk-1.4.19/
```
3.3. Configure
```
./configure
```
3.4. Select modules
```
make menuselect
```
3.5. Compile
```
make
```

3.6. Install
```
make install
```

3.7. Install the samples
```
make samples
```

3.8. Install the documentation
```
make progdocs
```

3.9. Install the script that starts Asterisk automatically
```
make config
```

4. Install asterisk-addons

4.1 Unpack asterisk-addons
```
tar -xvzf asterisk-addons-1.4.6.tar.gz
```

4.2. Change directory
```
cd asterisk-addons-1.4.6/
```

4.3. Configure
```
./configure
```

4.4. Select modules
```
make menuselect
```

4.5. Compile
```
make
```
4.6. Install
```
make install
```

4.7. Install the samples
```
make samples
```

5. Installing additional Spanish voices from the VoIPnovatos site.
5.1. Change to the directory where the sounds are located
```
cd /var/lib/asterisk/sounds/
```

5.2 Install the gsm core sounds
```
tar -xvzf /usr/local/src/voipnovatos-core-sounds-es-gsm-1.4.tar.gz
```

5.3. Install the g729 core sounds
```
tar -xvzf /usr/local/src/voipnovatos-core-sounds-es-g729-1.4.tar.gz
```

5.4. Install the gsm extra sounds
```
tar -xvzf /usr/local/src/voipnovatos-extra-sounds-es-gsm-1.4.tar.gz
```

5.5. Install the g729 extra sounds
```
tar -xvzf /usr/local/src/voipnovatos-extra-sounds-es-g729-1.4.tar.gz
```

5.6. Install Music on Hold in Spanish
```
tar -xvzf /usr/local/src/asterisk-voces-es-v1_2-moh-voipnovatos.tar.gz
```

After this, Asterisk is completely installed.
In the next post I will publish the configuration of the X100P card and the 
basic Asterisk configuration.