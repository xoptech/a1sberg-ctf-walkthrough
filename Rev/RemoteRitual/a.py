import subprocess
import string

# The hardcoded target string from ltrace
target = "50//6<;"
password = ""

print("Brute-forcing the ritual words...")

# Iterate through all 7 character positions
for i in range(len(target)):
    found_char = False
    for char in string.printable:
        if char in ['\n', '\r']: 
            continue
        
        # Build a 7-character test string
        test_input = password + char + "a" * (len(target) - len(password) - 1)
        
        # Run the binary through ltrace
        p = subprocess.Popen(["ltrace", "./ritual"], 
                             stdin=subprocess.PIPE, 
                             stderr=subprocess.PIPE, 
                             stdout=subprocess.PIPE, 
                             text=True)
        
        stdout, stderr = p.communicate(input=test_input + "\n")
        
        # Parse ltrace stderr for the strcmp line
        for line in stderr.split('\n'):
            if "strcmp(" in line:
                try:
                    # Extract the left side of strcmp("mutated", "50//6<;")
                    mutated = line.split('"')[1]
                    
                    # If the character at our current index matches the target, we found it!
                    if mutated[i] == target[i]:
                        password += char
                        print(f"Char {i+1} found: '{char}' -> Current password: {password}")
                        found_char = True
                        break # Break out of the ltrace parsing loop
                except IndexError:
                    pass
        
        # If we found the character, break out of the guessing loop to move to the next position
        if found_char:
            break

print(f"\n[+] The TRUE ritual words are: {password}")