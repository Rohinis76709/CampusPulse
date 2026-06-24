/* ============================================
   Campus Pulse - JavaScript
   Handles mobile menu, auto-hide alerts, table styling
   ============================================ */

// Toggle mobile navigation menu
function toggleMenu() {
    var nav = document.getElementById('navMenu');
    nav.classList.toggle('show');
}

// Close mobile menu when clicking outside
document.addEventListener('click', function(event) {
    var nav = document.getElementById('navMenu');
    var btn = document.querySelector('.mobile-menu-btn');
    if (btn && nav && !nav.contains(event.target) && !btn.contains(event.target)) {
        nav.classList.remove('show');
    }
});

// Header shadow effect on scroll
window.addEventListener('scroll', function() {
    var header = document.querySelector('.header');
    if (header) {
        if (window.scrollY > 50) {
            header.style.boxShadow = '0 4px 20px rgba(0,0,0,0.3)';
        } else {
            header.style.boxShadow = '0 2px 15px rgba(0,0,0,0.2)';
        }
    }
});

// Auto-hide messages after 4 seconds
document.addEventListener('DOMContentLoaded', function() {
    var alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.5s ease';
            setTimeout(function() {
                alert.style.display = 'none';
            }, 500);
        }, 4000);
    });

    // Zebra striping for tables
    var tableRows = document.querySelectorAll('.data-table tbody tr');
    tableRows.forEach(function(row, index) {
        if (index % 2 === 1) {
            row.style.background = 'rgba(0,0,0,0.02)';
        }
    });

    // Confirm before logout
    var logoutLinks = document.querySelectorAll('a.logout-btn');
    logoutLinks.forEach(function(link) {
        link.addEventListener('click', function(event) {
            if (!confirm('Are you sure you want to logout?')) {
                event.preventDefault();
            }
        });
    });
});
