document.addEventListener('DOMContentLoaded', function() {
    var menuToggle = document.getElementById('menuToggle');
    var nav = document.querySelector('.nav');
    if (menuToggle) {
        menuToggle.addEventListener('click', function() {
            nav.classList.toggle('open');
        });
    }
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.header')) {
            if (nav) nav.classList.remove('open');
        }
    });
    var tabs = document.querySelectorAll('.expertise-tab');
    tabs.forEach(function(tab) {
        tab.addEventListener('click', function() {
            tabs.forEach(function(t) { t.classList.remove('active'); });
            tab.classList.add('active');
            document.querySelectorAll('.expertise-content').forEach(function(c) { c.classList.remove('active'); });
            var target = document.getElementById('tab-' + tab.dataset.tab);
            if (target) target.classList.add('active');
        });
    });
});
