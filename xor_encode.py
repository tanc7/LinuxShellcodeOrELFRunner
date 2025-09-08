#!/usr/bin/env python3
import sys
import re

KEY = 0xAA  # example XOR key

# Read stdin (xxd -i output)
data = sys.stdin.read()

# Extract the byte values from the array
match = re.search(r'\{(.*)\}', data, re.DOTALL)
if not match:
    sys.exit("Failed to parse xxd output")

byte_str = match.group(1).replace('\n', '')
bytes_list = [int(b.strip(), 16) for b in byte_str.split(',') if b.strip()]

# XOR each byte
xor_bytes = [(b ^ KEY) for b in bytes_list]

# Generate C array
print("unsigned char payload[] = {")
for i, b in enumerate(xor_bytes):
    print(f"0x{b:02x},", end='')
    if (i + 1) % 16 == 0:
        print()
print("\n};")
print(f"unsigned int payload_len = {len(xor_bytes)};")
