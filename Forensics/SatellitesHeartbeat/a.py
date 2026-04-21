with open('deltas.txt', 'r') as f:
    lines = f.readlines()

binary_string = ""
for line in lines:
    val = float(line.strip())
    if val < 0.2:
        binary_string += "0"
    else:
        binary_string += "1"

# Split into 8-bit chunks and convert to ASCII
flag = ""
for i in range(0, len(binary_string), 8):
    byte = binary_string[i:i+8]
    flag += chr(int(byte, 2))

print("Recovered Flag:", flag)