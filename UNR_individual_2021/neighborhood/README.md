### The hint given is
```
Just moved into a new neighborhood and until my internet is set up I've been connected to an open network bun my friendly neighbor has set a password on it. I've captured some attempts for connection but I couldn't get the password can you help me? Flag format CTF{sha256(password)}.
```
and along side the challenge there is a file
```
neighborhood.pcap
```
\
Using `wireshark` and inspecting the file we can see three `EAPOL` packages. This gives me the idea of brute forcing the password using `aircrack-ng`
```
aircrack-ng -z -w /usr/share/wordlists/rockyou.txt neighborhood.pcap 
```
with the result
```
Reading packets, please wait...
Opening neighborhood.pcap
Read 4 packets.

   #  BSSID              ESSID                     Encryption

   1  DC:A6:32:AC:DA:6B  test-raspi                WPA (1 handshake)

Choosing first network as target.

Reading packets, please wait...
Opening neighborhood.pcap
Read 4 packets.

1 potential targets



                               Aircrack-ng 1.6 

      [00:00:00] 1234/10303727 keys tested (4099.56 k/s) 

      Time left: 41 minutes, 53 seconds                          0.01%

                          KEY FOUND! [ mickeymouse ]


      Master Key     : 38 1B CF B7 B7 2C C4 31 C8 25 1F 27 75 EB CF 3B 
                       F3 F6 79 93 A4 94 9D 09 A7 76 41 5D 40 85 2B F6 

      Transient Key  : A7 17 E4 1F B9 4C BA 47 B4 7D 1D 65 E9 EC 28 97 
                       7F 64 4A B7 43 A8 4F 87 16 2F 8E 07 9F 02 18 D5 
                       B2 6C FE 20 A7 BD C7 D1 5B 05 80 1F 32 23 92 0A 
                       F1 73 F4 51 F5 5A 22 7E 3F D8 0E 9C 84 47 D1 91 

      EAPOL HMAC     : ED BF 01 1B CB C6 19 4B 8B 84 7E 43 6E 5A CC 4F 
```
\
All that is left to do is make the password `mickeymouse` into sha256
```
echo -n "mickeymouse" | sha256sum
```
with the output
```
d0ff2794ec7af8764a654b31b68d07aec0f518053fee9629917a5782ad9cf837
```
### Our flag is
```
CTF{d0ff2794ec7af8764a654b31b68d07aec0f518053fee9629917a5782ad9cf837}
```
