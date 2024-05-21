// Load this script on all pages
$(function () {
    // Authentication scripts
    setTimeout(function () {
        $('#flash-message').fadeOut('slow', function () {
            $(this).remove();
        });
    }, 6000);


    // Registering a business page
    // Adding a new business location
    $.ajax({
        url: "https://maps.googleapis.com/maps/api/js?key=AIzaSyB7DvaMrr77CKuCqUnQ2xQTQ3WKbAwgCMw&callback=initMap",
        dataType: "script",
    });


    // submiting business details for registration
    let form = $('#register-bs');
    data = form.serialize();
    console.log(data+ 'heyyyyy');
    $('#register-bs').submit(function (e) {
        e.preventDefault();


        let form = $(this);
        console.log(form);
    });





















    $('.form-control').on('input', function () {
        // Find the corresponding form-text element based on the input's aria-describedby attribute
        const ariaDescribedBy = $(this).attr('aria-describedby');
        const charCountElement = $('#' + ariaDescribedBy);

        // Get the current length of the input's value
        const currentLength = $(this).val().length;

        // Update the text of the form-text element with the character count
        charCountElement.text(`Entered: ${currentLength} characters.`);
    });


    $('.mb-3 input, .mb-3 textarea, .mb-3 select').focus(function () {
        $(this).closest('.mb-3').addClass('focus-highlight');
    });
    $('.mb-3 input, .mb-3 textarea, .mb-3 select').blur(function () {
        $(this).closest('.mb-3').removeClass('focus-highlight');
    });

    $('.latitude-dv, .longitude-dv').find('input').focus(function () {
        $(this).closest('.col').addClass('focus-highlight');
    });

    $('.latitude-dv, .longitude-dv').find('input').blur(function () {
        $(this).closest('.col').removeClass('focus-highlight');
    });
});


// callback function for google maps api
function initMap() {
    const mapElement = $("#map").get(0);
    const map = new google.maps.Map(mapElement, {
        center: { lat: -3.8825, lng: 39.6211 },
        disableDefaultUI: true,
        gestureHandling: "cooperative",
        mapTypeId: 'hybrid',
        zoom: 10,
    });

    map.addListener('click', function (e) {
        $('.latitude-dv').find('input').val(e.latLng.lat());
        $('.longitude-dv').find('input').val(e.latLng.lng());

        const marker = new google.maps.Marker({
            position: { lat: clickedLat, lng: clickedLng },
            map: map,
            title: "Clicked Location",
        });
    });
}