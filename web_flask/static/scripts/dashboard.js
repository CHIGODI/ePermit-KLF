// JavaScript code to rotate testimonials
document.addEventListener('DOMContentLoaded', () => {
    const testimonials = document.querySelector('.testimonials');
    const testimonialItems = document.querySelectorAll('.testimonial');
    let currentIndex = 0;
    const intervalTime = 3000; // 3 seconds

    function rotateTestimonials() {
        testimonials.style.transition = 'none';
        testimonials.style.transform = `translateX(0)`;
        currentIndex = 0;

        setInterval(() => {
            currentIndex++;
            testimonials.style.transition = 'transform 1s ease-in-out';
            testimonials.style.transform = `translateX(-${currentIndex * 100}%)`;

            if (currentIndex === testimonialItems.length) {
                setTimeout(() => {
                    testimonials.style.transition = 'none';
                    testimonials.style.transform = `translateX(0)`;
                    currentIndex = 0;
                }, 1000);
            }
        }, intervalTime);
    }

    rotateTestimonials();
});
