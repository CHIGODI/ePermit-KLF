$(function () {

    // Authentication scripts
    setTimeout(function () {
        $('#flash-message').fadeOut('slow', function () {
            $(this).remove();
        });
    }, 6000);

    $('.form-auth').on('submit', function (e) {
        // Iterate over each input field in the form
        $(this).find('input').each(function () {
            if ($(this).val() == '') {
                $(this).addClass('is-invalid');
            }
            if ($(this).val() != '') {
                $(this).removeClass('is-invalid');
            }
        });
    });



























    let apiKey = "AIzaSyB7DvaMrr77CKuCqUnQ2xQTQ3WKbAwgCMw";
    let apiUrl = "https://maps.googleapis.com/maps/api/js?key=" + apiKey + "&callback=initMap";

    let scriptTag = document.createElement('script');
    scriptTag.async = true;
    scriptTag.defer = true;
    scriptTag.src = apiUrl;
    $('head').append(scriptTag);

    $('.form-control').on('input', function () {
        // Find the corresponding form-text element based on the input's aria-describedby attribute
        const ariaDescribedBy = $(this).attr('aria-describedby');
        const charCountElement = $('#' + ariaDescribedBy);

        // Get the current length of the input's value
        const currentLength = $(this).val().length;

        // Update the text of the form-text element with the character count
        charCountElement.text(`Entered: ${currentLength} characters.`);
    });


    $('.mb-3 input, .mb-3 text-area, row').focus(function () {
        $(this).closest('.mb-3').addClass('focus-highlight');
    });
    $('.mb-3 input, .mb-3 text-area, .row').blur(function () {
        $(this).closest('.mb-3').removeClass('focus-highlight');
    });






});

function initMap() {
    let map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: -3.9458, lng: 39.5364 },
        zoom: 8
    });
}

