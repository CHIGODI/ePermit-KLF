// Rotate testimonials
let testimonials = document.querySelectorAll('.testimonial');
let currentIndex = 0;

function rotateTestimonials() {
    setInterval(() => {
        testimonials[currentIndex].classList.remove('active');
        currentIndex = (currentIndex + 1) % testimonials.length;
        testimonials[currentIndex].classList.add('active');
    }, 5000); // Change testimonial every 5 seconds
}

// Initially show first testimonial
testimonials[currentIndex].classList.add('active');
rotateTestimonials();
