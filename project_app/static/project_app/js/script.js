function myMenuFunction() {
    var i = document.getElementById("navMenu");

    if (i.className === "nav-menu") {
        i.className += " responsive";
    } else {
        i.className = "nav-menu";
    }
}

var a = document.getElementById("loginBtn");
var b = document.getElementById("registerBtn");
var x = document.getElementById("login");
var y = document.getElementById("register");

function logiin() {
    x.style.left = "4px";
    y.style.right = "-520px";
    a.className += " white-btn";
    b.className = "btn";
    x.style.opacity = 1;
    y.style.opacity = 0;
}

function regiister() {
    x.style.left = "-510px";
    y.style.right = "5px";
    a.className = "btn";
    b.className += " white-btn";
    x.style.opacity = 0;
    y.style.opacity = 1;
}


function login() {
    var username = document.getElementById('login-username').value;
    var password = document.getElementById('login-password').value;

    $.ajax({
        url: '/api/login/',
        method: 'POST',
        data: { username: username, password: password },
        success: function (response) {
            console.log('Login successful:', response);
            // Redirect or perform other actions after successful login
            window.location.href = '/student_dash/';
        },
        error: function (error) {
            console.error('Login failed:', error.responseJSON);
        }
    });
}

function register() {
    var username = document.getElementById('signup-username').value;
    var email = document.getElementById('signup-email').value;
    var password = document.getElementById('signup-password').value;
    var confirmPassword = document.getElementById('signup-password2').value;
    var role = document.querySelector('input[name="select"]:checked').value;

    // Additional validation can be added as needed

    if (password !== confirmPassword) {
        console.error('Passwords do not match');
        return;
    }

    $.ajax({
        url: '/api/register/',
        method: 'POST',
        data: {
            username: username,
            email: email,
            password: password,
            role: role,
            enrollments: [],
            grades: [],
            interaction_histories: [],
            submissions: []
        },
        success: function (response) {
            console.log('Registration successful:', response);

            // Assuming the response contains the user's role
            var userRole = response.role;

            // Redirect based on the user's role
            if (userRole === 'admin') {
                window.location.href = '/admin_dashboard/';
            } else if (userRole === 'teacher') {
                window.location.href = '/teacher_dashboard/';
            } else if (userRole === 'student') {
                window.location.href = '/student_dashboard/';
            } else {
                console.error('Unknown user role:', userRole);
            }
        },
        error: function (error) {
            console.error('Registration failed:', error.responseJSON);
        }
    });
}
