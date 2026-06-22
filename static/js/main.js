document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('menuToggle');
    const nav = document.querySelector('.nav');
    if (menuToggle) {
        menuToggle.addEventListener('click', function() {
            nav.classList.toggle('open');
        });
    }
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.header')) {
            nav.classList.remove('open');
        }
    });
});
