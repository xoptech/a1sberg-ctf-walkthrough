import socket

# Use lowercase for the prompts to avoid case-sensitivity issues
rules = {
    "mia: sorry": "I Love You",
    "mia: i love you": "Sorry",
    "mia: fuck you": "Oh Fuck",
    "mia: oh fuck": "Fuck You"
}

s = socket.create_connection(('178.128.110.55', 5206))

while True:
    data = s.recv(4096).decode()
    
    if not data:
        break
        
    print(data, end="")
    
    # Only evaluate and respond if it's our turn to type
    if "You:" in data:
        data_lower = data.lower()
        
        # Isolate the most recent line from Mia to ignore the banner rules
        last_mia_index = data_lower.rfind("mia: ")
        
        if last_mia_index != -1:
            recent_prompt = data_lower[last_mia_index:]
            
            # Check the recent prompt against our rules
            for prompt, reply in rules.items():
                if prompt in recent_prompt:
                    s.sendall(f"{reply}\n".encode())
                    break