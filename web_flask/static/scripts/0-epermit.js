// Load this script on all pages
$(function () {
    // Authentication scripts
    setTimeout(function () {
        $('#flash-message').fadeOut('slow', function () {
            $(this).remove();
        });
    }, 6000);


    // Registering a business page
    $('.form-control').on('input', function () {
        // Find the corresponding form-text element based on the input's aria-describedby attribute
        const ariaDescribedBy = $(this).attr('aria-describedby');
        const charCountElement = $('#' + ariaDescribedBy);

        // Get the current length of the input's value
        const currentLength = $(this).val().length;

        // Update the text of the form-text element with the character count
        charCountElement.text(`Entered: ${currentLength} characters.`);
    });


    $('.mb input, .mb textarea, .mb select').focus(function () {
        $(this).closest('.mb').addClass('focus-highlight');
    });
    $('.mb input, .mb textarea, .mb select').blur(function () {
        $(this).closest('.mb').removeClass('focus-highlight');
    });

    $('.latitude-dv, .longitude-dv').find('input').focus(function () {
        $(this).closest('.col').addClass('focus-highlight');
    });

    $('.latitude-dv, .longitude-dv').find('input').blur(function () {
        $(this).closest('.col').removeClass('focus-highlight');
    });

    // Adding a new business location
    $.ajax({
        url: "https://maps.googleapis.com/maps/api/js?key=AIzaSyB7DvaMrr77CKuCqUnQ2xQTQ3WKbAwgCMw&callback=initMap",
        dataType: "script",
    });


    // submiting business details for registration
    $('.').click(function (e) {

        //
        let business_registration_data = {}
        let owner_info = {}


        let rawBusinessFormData = $(this).serializeArray();
        let rawOwnerFormData = $(this).serializeArray();


        $.each(rawBusinessFormData, function (index, obj) {
            business_registration_data[obj.name] = obj.value;
        });

        $.ajax({
            url: "http://localhost:5003/api/v1/businesses",
            type: "POST",
            data: JSON.stringify(business_registration_data),
            contentType: "application/json",
            success: function (data) {
                console.log(data);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log("Error: ", textStatus, errorThrown);  // Log error details
            }
        });

        $.each(rawOwnerFormData, function (index, obj) {
            owner_info[obj.name] = obj.value;
        });

        $.ajax({
            url: "http://localhost:5003/api/v1/users",
            type: "PUT",
            data: JSON.stringify(owner_info),
            contentType: "application/json",
            success: function (data) {
                console.log(data);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log("Error: ", textStatus, errorThrown);  // Log error details
            }
        });
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