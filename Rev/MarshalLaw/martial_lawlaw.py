def decode():
    data = [4, 103, 48, 23, 20, 62, 101, 21, 69, 10, 167, 139, 141, 198, 136, 215, 249, 149, 199, 198, 22, 61, 87, 31, 0]
    
    flag = ''
    
    for i, b in enumerate(data):
        key = (((i * 13) + 7) ^ 66) & 255
        flag += chr(b ^ key)
        
    return flag

print(decode())