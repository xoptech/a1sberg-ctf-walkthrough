import subprocess

print("Brute-forcing the 32-character hex key...")
hex_chars = "0123456789abcdef"
password = ""

for i in range(16): # 16 bytes (32 hex characters)
    found = False
    for c1 in hex_chars:
        for c2 in hex_chars:
            test_byte = c1 + c2
            
            # Pad our current guess to exactly 32 characters with zeroes
            test_input = password + test_byte + "0" * (32 - len(password) - 2)
            
            p = subprocess.Popen(["ltrace", "./challs_unpacked"], 
                                 stdin=subprocess.PIPE, 
                                 stderr=subprocess.PIPE, 
                                 stdout=subprocess.PIPE, 
                                 text=True)
            
            stdout, stderr = p.communicate(input=test_input + "\n")
            
            # Check for the win condition!
            if "Access Granted" in stdout or "Access Granted" in stderr:
                password += test_byte
                print(f"\n[+] BOOM! Access Granted! The full hex key is: {password}")
                exit(0)
                
            # Count the number of times sscanf was executed in ltrace output
            sscanf_count = stderr.count("sscanf")
            
            # If sscanf was called more times than our current byte index (i+1),
            # it means this byte passed the internal check!
            if sscanf_count > i + 1:
                password += test_byte
                print(f"Byte {i+1}/16 found: '{test_byte}' -> Current key: {password}")
                found = True
                break
        if found:
            break

print("Script finished.")