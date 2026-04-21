let currentUsername = '';
let currentFlag = '';

function switchTab(tabName) {
    const tabs = document.querySelectorAll('.tab');
    const registerForm = document.getElementById('register-form');
    const loginForm = document.getElementById('login-form');

    tabs.forEach(tab => {
        tab.classList.remove('active');
    });

    if (tabName === 'register') {
        event.target.classList.add('active');
        registerForm.classList.add('active');
        loginForm.classList.remove('active');
    } else {
        event.target.classList.add('active');
        loginForm.classList.add('active');
        registerForm.classList.remove('active');
    }

    clearMessages();
}

function clearMessages() {
    const messages = document.querySelectorAll('.message');
    messages.forEach(msg => {
        msg.style.display = 'none';
        msg.textContent = '';
        msg.className = 'message';
    });
}

function showMessage(formType, message, isError = true) {
    const messageDiv = document.getElementById(`${formType}-message`);
    messageDiv.textContent = message;
    messageDiv.className = `message ${isError ? 'error' : 'success'}`;
    messageDiv.style.display = 'block';

    if (!isError) {
        setTimeout(() => {
            messageDiv.style.display = 'none';
        }, 3000);
    }
}

function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type}`;
    toast.classList.add('show');

    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

function setLoading(button, isLoading) {
    if (isLoading) {
        button.disabled = true;
        const originalText = button.textContent;
        button.setAttribute('data-original-text', originalText);
        button.innerHTML = 'Processing <span class="loading"></span>';
    } else {
        button.disabled = false;
        const originalText = button.getAttribute('data-original-text');
        if (originalText) {
            button.textContent = originalText;
        }
    }
}

function showRegistrationModal() {
    const modal = document.getElementById('registerModal');
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeModal() {
    const modal = document.getElementById('registerModal');
    modal.classList.remove('active');
    document.body.style.overflow = '';

    const loginTab = document.querySelectorAll('.tab')[1];
    loginTab.click();
    document.getElementById('reg-username').value = '';
}

function showDashboard(username, flag) {
    currentUsername = username;
    currentFlag = flag;

    document.getElementById('authContainer').style.display = 'none';
    document.getElementById('dashboardContainer').style.display = 'block';

    document.getElementById('dashboardUsername').textContent = username;

    const now = new Date();
    const timeString = now.toLocaleTimeString();
    document.getElementById('sessionTime').textContent = timeString;

    document.getElementById('flagPlaceholder').style.display = 'none';
    document.getElementById('flagValue').style.display = 'block';
    document.getElementById('flagCode').textContent = flag;

    addActivity('Authentication successful', timeString);

    showToast(`Welcome back, ${username}!`, 'success');
}

function logout() {
    document.getElementById('dashboardContainer').style.display = 'none';
    document.getElementById('authContainer').style.display = 'block';

    document.getElementById('login-username').value = '';
    document.getElementById('login-password').value = '';
    document.getElementById('reg-username').value = '';

    clearMessages();

    showToast('Signed out successfully', 'success');

    currentUsername = '';
    currentFlag = '';
}

function addActivity(action, time = null) {
    const activityList = document.getElementById('activityList');
    const activityItem = document.createElement('div');
    activityItem.className = 'activity-item';

    const activityTime = document.createElement('span');
    activityTime.className = 'activity-time';
    activityTime.textContent = time || new Date().toLocaleTimeString();

    const activityText = document.createElement('span');
    activityText.className = 'activity-text';
    activityText.textContent = action;

    activityItem.appendChild(activityTime);
    activityItem.appendChild(activityText);

    activityList.insertBefore(activityItem, activityList.firstChild);

    while (activityList.children.length > 10) {
        activityList.removeChild(activityList.lastChild);
    }
}

function copyFlag() {
    const flag = document.getElementById('flagCode').textContent;
    navigator.clipboard.writeText(flag).then(() => {
        showToast('Flag copied to clipboard!', 'success');
    }).catch(() => {
        showToast('Failed to copy flag', 'error');
    });
}

async function handleRegistration(event) {
    event.preventDefault();

    const username = document.getElementById('reg-username').value.trim();
    const submitBtn = event.target.querySelector('button[type="submit"]');

    if (!username) {
        showMessage('register', 'Please enter a username', true);
        return;
    }

    setLoading(submitBtn, true);
    clearMessages();

    try {
        const formData = new FormData();
        formData.append('username', username);

        const response = await fetch('/register', {
            method: 'POST',
            body: formData
        });

        const result = await response.text();

        if (result.includes('User exists')) {
            showMessage('register', 'Username already exists', true);
        } else if (result.includes('User registered')) {
            showRegistrationModal();
        } else {
            showMessage('register', 'Registration failed', true);
        }
    } catch (error) {
        showMessage('register', 'Network error', true);
    } finally {
        setLoading(submitBtn, false);
    }
}

async function handleLogin(event) {
    event.preventDefault();

    const username = document.getElementById('login-username').value.trim();
    const password = document.getElementById('login-password').value;
    const submitBtn = event.target.querySelector('button[type="submit"]');

    if (!username || !password) {
        showMessage('login', 'Please enter both username and password', true);
        return;
    }

    setLoading(submitBtn, true);
    clearMessages();

    try {
        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);

        const response = await fetch('/login', {
            method: 'POST',
            body: formData
        });

        const result = await response.text();

        const flagPattern = /(CTF\{[^}]+\}|A1S\{[^}]+\}|flag\{[^}]+\}|[A-Z0-9]+\{[^}]+\})/i;
        const flagMatch = result.match(flagPattern);

        if (result.includes('Wrong password')) {
            showMessage('login', 'Invalid credentials', true);
        } else if (result.includes('Invalid')) {
            showMessage('login', 'Invalid username', true);
        } else if (flagMatch) {
            const flag = flagMatch[0];
            showMessage('login', 'Authentication successful', false);

            setTimeout(() => {
                showDashboard(username, flag);
            }, 500);
        } else if (result.includes('User registered')) {
            showMessage('login', 'Please register first', true);
        } else {
            if (result.includes('{') && result.includes('}')) {
                const flag = result.trim();
                showMessage('login', 'Authentication successful', false);
                setTimeout(() => {
                    showDashboard(username, flag);
                }, 500);
            } else {
                showMessage('login', 'Authentication failed: ' + result.substring(0, 100), true);
            }
        }
    } catch (error) {
        console.error('Login error:', error);
        showMessage('login', 'Network error: ' + error.message, true);
    } finally {
        setLoading(submitBtn, false);
    }
}

document.addEventListener('click', function(event) {
    const modal = document.getElementById('registerModal');
    if (event.target === modal) {
        closeModal();
    }
});

document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        const modal = document.getElementById('registerModal');
        if (modal.classList.contains('active')) {
            closeModal();
        }
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.getElementById('registerForm');
    const loginForm = document.getElementById('loginForm');

    if (registerForm) {
        registerForm.addEventListener('submit', handleRegistration);
    }

    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }

    const inputs = document.querySelectorAll('input');
    inputs.forEach(input => {
        input.addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                const form = this.closest('form');
                if (form) {
                    form.dispatchEvent(new Event('submit'));
                }
            }
        });
    });
});
