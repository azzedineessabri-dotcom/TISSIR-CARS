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

    // Search form: default dates
    const searchForm = document.querySelector('.search-form');
    if (searchForm) {
        const now = new Date();
        const today = now.toISOString().split('T')[0];
        const pickupDate = searchForm.querySelector('[name="date_debut"]');
        const returnDate = searchForm.querySelector('[name="date_fin"]');
        if (pickupDate && !pickupDate.value) pickupDate.value = today;
        if (returnDate && !returnDate.value) {
            const later = new Date(now.getTime() + 3 * 24 * 60 * 60 * 1000);
            returnDate.value = later.toISOString().split('T')[0];
        }
    }

    const bookingForm = document.getElementById('bookingForm');
    if (bookingForm) {
        bookingForm.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.textContent = 'Traitement en cours...';
            }
        });
    }

});
