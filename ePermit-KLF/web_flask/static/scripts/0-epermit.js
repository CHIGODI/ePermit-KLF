$(function () {
    let apiKey = "AIzaSyB7DvaMrr77CKuCqUnQ2xQTQ3WKbAwgCMw";
    let apiUrl = "https://maps.googleapis.com/maps/api/js?key=" + apiKey + "&callback=initMap";

    let scriptTag = document.createElement('script');
    scriptTag.async = true;
    scriptTag.defer = true; 
    scriptTag.src = apiUrl;
    $('head').append(scriptTag);


    $('input[type="name"], input[type="vat"]').on('input', function () {
        const currentLength = $(this).val().length;
        $('#charCount').text(`Currently Entered:  ${currentLength} characters.`);
    });
});

function initMap() {
    let map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: -3.9458, lng: 39.5364 },
        zoom: 8
    });
}

