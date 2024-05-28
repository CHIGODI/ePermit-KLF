const faqs = document.querySelectorAll(".faq");
faqs.forEach(faq => {
    faq.addEventListener("click", () => {
        faq.classList.toggle("active");
    })
})

document.getElementById('contactForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the form from submitting the traditional way

    // Capture form data
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const subject = document.getElementById('subject').value;
    const message = document.getElementById('message').value;

    // Optionally, you can send the form data to your server here using fetch or XMLHttpRequest

    // Show the popup message
    const popupMessage = document.getElementById('popupMessage');
    popupMessage.style.display = 'block';

    // Hide the popup message after a few seconds
    setTimeout(function() {
        popupMessage.style.display = 'none';
    }, 5000); // Adjust the timeout duration as needed

    // Clear the form fields
    document.getElementById('contactForm').reset();
});
