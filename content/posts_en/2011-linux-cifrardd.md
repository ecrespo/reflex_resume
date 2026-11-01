Title: How to encrypt directories/partitions with eCryptfs
Date: 2011-08-21 09:00
Category: Tutorial de Linux
Tags: Linux,Debian, Ubuntu, Canaima,Seguridad,eCryptfs
lang: en
translation: true

This article is based on the HowtoForge article on the same [topic](http://www.howtoforge.net/how-to-encrypt-directories-partitions-with-ecryptfs-on-debian-squeeze).

The idea is to encrypt the user's home directory, so that the encrypted directory is mounted automatically when the computer boots.

You need a backup of the user's folder to avoid data loss if you forget the passphrase.

1. Install eCryptfs:

Run:

```
aptitude install ecryptfs-utils
```

2. Encrypt a directory.

Back up the files and directories in the user's home:

```
cp -pfr /home/ecrespo /tmp/

```

Encrypt the /home/ecrespo/ directory by mounting the ecryptfs file system:

Select aes, 16, do not enable plaintext passthrough, do not enable filename encryption, so with these options you only need to press enter at every prompt when mounting the encrypted partition.

```
mount -t ecryptfs /home/ecrespo /home/ecrespo

Passphrase:
Select cipher:
 1) aes: blocksize = 16; min keysize = 16; max keysize = 32 (not loaded)
 2) blowfish: blocksize = 16; min keysize = 16; max keysize = 56 (not loaded)
 3) des3_ede: blocksize = 8; min keysize = 24; max keysize = 24 (not loaded)
 4) twofish: blocksize = 16; min keysize = 16; max keysize = 32 (not loaded)
 5) cast6: blocksize = 16; min keysize = 16; max keysize = 32 (not loaded)
 6) cast5: blocksize = 8; min keysize = 5; max keysize = 16 (not loaded)
Selection [aes]:
Select key bytes:
 1) 16
 2) 32
 3) 24
Selection [16]:
Enable plaintext passthrough (y/n) [n]: Enter
Enable filename encryption (y/n) [n]: Enter
Attempting to mount with the following options:
  ecryptfs_unlink_sigs
  ecryptfs_key_bytes=16
  ecryptfs_cipher=aes
  ecryptfs_sig=162827f20fdadf4e
Mounted eCryptfs
```

3. Check that the partition has been mounted.

The mount command only returns the partitions that are mounted on the Linux system.

```
mount /home/ecrespo on /home/ecrespo type ecryptfs (rw,ecryptfs_sig=162827f20fdadf4e,ecryptfs_cipher=aes,ecryptfs_key_bytes=16,ecryptfs_unlink_sigs)
```

4. Restore the backup and delete the backup from the /tmp/ directory

```
cp -pfr /tmp/ecrespo /home/
rm -fr /tmp/ecrespo
```

5. Check that file encryption works.

For testing purposes, a file from /etc/ is copied to the user's home.
Show the contents of the hostname file in /etc/

```
cat /etc/hostname 
canaima-popular
```

Copy the hostname file to the user's home:

```
cp /etc/hostname /home/ecrespo/
```

While the encrypted partition is mounted you can view the files:

```
cat /home/ecrespo/hostname 
canaima-popular
```

Unmount the partition.

```
umount /home/ecrespo/
```

Check that the file is encrypted:

```
cat /home/ecrespo/hostname
4��ˉ�s|| � "3DUfw`�6���D �̬�����{� _CONSOLE ('��N�pD���-� \ٛn�Ś/��TD��xҝD[:�$] �wq�V��
�n /�k�a:�H.�{ USj�@u)�c ������T� �� �m�иや� � Z�&��0�Q��B�� /��q�e��E��li�"dx�tDs���k����h�J��20��&T�?R�x� �W�$�
                                                                                                                   �$�@ �&
                                                                                                                           ��� �G� /�.L���1d�� j����{cYRꄙZ`��t 8�4ԬZ~ ,)H
eb �� f ��?��
          �_' ��K&�d)����{y�z����ֆ�2x��h�� &j���tuq��a�JeJ�� ���\"~
                                                                   ��5`� V RCB`��������PU�&������X�
                                                                                                    9Ԥ[� 4O.� �� ̔�;/ �����#j V`Sf^��<�uB8 �ЭIx�4PR�� dml��`&c �
! ҟ&`�~�U?u�� �����쵮 @�)�8�Q U��杞M�e��="�}�V# ��>������ �>�F�� R�#ZgI���^J�� ,��0ݼR�rO�f��AxS��3�\�M���o�D �u�Av)�qq%�(F�/���%tL��w�U�k6~c��` “=�4N��E�= #� � a7�����v�(V�p�HlR�Y5����#^���K �~ :h��Z�Q�J�{�FC�N;*� 0Bő*���=�
�ՙ��R�mќet ���7B�_�Dz.[�6>�ĸؓ�� �Nc��#��NR��@� 4 �/���M?Om �|;/�Oe9�6��&6D*U�A�e��� �V
�ZM�<ɝ��"�0��0�WŸL�H�,r
                        �>��f��4�$�wA�rѫ� �0H�����CP�i��&���!b���-#
$ލ;�X!y�� ~� I5e��V|Y�\� �H^£�7�0�Z��{�}"!��͡�� 6�M�!LNȆXvF         )� ��G�Nuɍ� � ӧ��s���t ���t��o&� C������W�#��Cpk�><„
```

6. Automatically mount the partition or directory.

Plug in a pendrive and run the fdisk -l command, where the pendrive's partition will appear:

```
fdisk -l
 Disk /dev/sdb: 16.0 GB, 16011542528 bytes
32 heads, 63 sectors/track, 15512 cylinders, 31272544 sectores en total
Units = sectores of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Identificador del disco: 0x59a4123d

Disposit. Inicio    Comienzo      Fin      Bloques  Id  Sistema
/dev/sdb1   *          63    31272191    15636064+   b  W95 FAT32
```

Mount the pendrive:

```
mkdir /mnt/usb
mount /dev/sdb1 /mnt/usb
```

Running mount will only show the partitions mounted on the computer:

```
mount /dev/sdb1 on /mnt/usb type vfat (rw)
```

Unlike the original article, the pendrive and the encrypted partition are not mounted automatically.



===

Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
