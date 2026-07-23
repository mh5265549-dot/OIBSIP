// Utility function to hash passwords using SHA-256
async function hashPassword(password) {
    const msgBuffer = new TextEncoder().encode(password);
    const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}

document.addEventListener('DOMContentLoaded', () => {
    const path = window.location.pathname;

    // --- REGISTRATION LOGIC ---
    const registerBtn = document.getElementById('registerBtn');
    if (registerBtn) {
        registerBtn.addEventListener('click', async () => {
            const emailInput = document.getElementById('regEmail').value.trim();
            const passInput = document.getElementById('regPassword').value;
            const errorMsg = document.getElementById('errorMsg');
            const successMsg = document.getElementById('successMsg');

            errorMsg.classList.add('hidden');
            successMsg.classList.add('hidden');

            // Basic validation: non-empty
            if (!emailInput || !passInput) {
                errorMsg.textContent = "Error: All fields are required.";
                errorMsg.classList.remove('hidden');
                return;
            }

            // Password policy validation: min 8 chars, at least 1 number
            const hasNumber = /\d/;
            if (passInput.length < 8 || !hasNumber.test(passInput)) {
                errorMsg.textContent = "Error: Password must be at least 8 characters long and contain at least 1 number.";
                errorMsg.classList.remove('hidden');
                return;
            }

            let users = JSON.parse(localStorage.getItem('registeredUsers')) || [];

            // Duplicate user check
            const userExists = users.some(u => u.email === emailInput);
            if (userExists) {
                errorMsg.textContent = "Error: A user with this email or username already exists.";
                errorMsg.classList.remove('hidden');
                return;
            }

            // Secure hash generation
            const hashedPassword = await hashPassword(passInput);

            users.push({ email: emailInput, password: hashedPassword });
            localStorage.setItem('registeredUsers', JSON.stringify(users));

            successMsg.textContent = "Registration successful! Redirecting to login...";
            successMsg.classList.remove('hidden');

            setTimeout(() => {
                window.location.href = 'login.html';
            }, 1500);
        });
    }

    // --- LOGIN LOGIC ---
    const loginBtn = document.getElementById('loginBtn');
    if (loginBtn) {
        loginBtn.addEventListener('click', async () => {
            const emailInput = document.getElementById('loginEmail').value.trim();
            const passInput = document.getElementById('loginPassword').value;
            const errorMsg = document.getElementById('errorMsg');

            errorMsg.classList.add('hidden');

            if (!emailInput || !passInput) {
                errorMsg.textContent = "Error: All fields are required.";
                errorMsg.classList.remove('hidden');
                return;
            }

            const users = JSON.parse(localStorage.getItem('registeredUsers')) || [];
            const hashedPassword = await hashPassword(passInput);

            // Generic credential verification (do not reveal if username or password was specifically wrong)
            const matchedUser = users.find(u => u.email === emailInput && u.password === hashedPassword);

            if (!matchedUser) {
                errorMsg.textContent = "Error: Invalid username or password.";
                errorMsg.classList.remove('hidden');
                return;
            }

            // Set active session
            localStorage.setItem('activeSession', JSON.stringify({ email: matchedUser.email }));
            window.location.href = 'dashboard.html';
        });
    }

    // --- DASHBOARD GUARD & LOGOUT LOGIC ---
    if (path.includes('dashboard.html')) {
        const session = JSON.parse(localStorage.getItem('activeSession'));
        if (!session || !session.email) {
            // Protected page redirect if accessed without session
            window.location.href = 'login.html';
            return;
        }

        const userDisplay = document.getElementById('userDisplay');
        if (userDisplay) {
            userDisplay.textContent = session.email;
        }

        const logoutBtn = document.getElementById('logoutBtn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', () => {
                localStorage.removeItem('activeSession');
                window.location.href = 'login.html';
            });
        }
    }
});
