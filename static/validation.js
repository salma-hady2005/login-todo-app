document.addEventListener("DOMContentLoaded", function () {
    
    const registerForm = document.querySelector("#register-form");


    if (registerForm) {
        registerForm.addEventListener("submit", function (event) {
            
            const name = document.querySelector("#name").value.trim();
            const email = document.querySelector("#email").value.trim();
            const password = document.querySelector("#password").value;
            const confirmPassword =
                document.querySelector("#confirm_password").value;

            let error = "";

            if (!name) {
                error = "Name is required";
            } else if (!email) {
                error = "Email is required";
            } else if (!password) {
                error = "Password is required";
            } else if (!confirmPassword) {
                error = "Confirm password is required";
            } else if (password !== confirmPassword) {
                error = "Passwords do not match";
            }

            if (error) {
                event.preventDefault();
                alert(error);
            }
        });
    }

    const loginForm = document.querySelector("#login-form");

    if (loginForm) {
        loginForm.addEventListener("submit", function (event) {
            const email = document.querySelector("#email").value.trim();
            const password = document.querySelector("#password").value;

            let error = "";

            if (!email) {
                error = "Email is required";
            } else if (!password) {
                error = "Password is required";
            }

            if (error) {
                event.preventDefault();
                alert(error);
            }
        });
    }

    const todoForm = document.querySelector("#todo-form");

    if (todoForm) {
        todoForm.addEventListener("submit", function (event) {
            const title = document.querySelector("#title").value.trim();

            let error = "";

            if (!title) {
                error = "Title is required";
            } else if (title.length > 200) {
                error = "Title is too long";
            }

            if (error) {
                event.preventDefault();
                alert(error);
            }
        });
    }
});
// Dark mode toggle
document.addEventListener("DOMContentLoaded", function () {
    const themeButtons = document.querySelectorAll(".theme-toggle");

    // Load the saved theme
    if (localStorage.getItem("theme") === "dark") {
        document.body.classList.add("dark-mode");
    }

    function updateButtonText() {
        const isDark = document.body.classList.contains("dark-mode");

        themeButtons.forEach(function (button) {
            button.textContent = isDark ? "☀️ Light Mode" : "🌙 Dark Mode";
        });
    }

    updateButtonText();

    themeButtons.forEach(function (button) {
        button.addEventListener("click", function () {
            document.body.classList.toggle("dark-mode");

            const isDark = document.body.classList.contains("dark-mode");

            localStorage.setItem("theme", isDark ? "dark" : "light");

            updateButtonText();
        });
    });
});