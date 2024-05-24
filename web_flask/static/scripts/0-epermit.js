// Load this script on all pages
$(function () {
    apiKey =''

    // Adding a map for location
    $.ajax({
        url: 'https://maps.googleapis.com/maps/api/js?key=' + apiKey + '&callback=initMap',
        dataType: "script",
    });

    // Alert timeouts
    setTimeout(function () {
        $('#flash-message, #flash-form-error').fadeOut('slow', function () {
            $(this).remove();
        });
    }, 8000);

    // Registering a business page
    // counts characters as user fills in register bs
    $('.form-control').on('input', function () {
        const ariaDescribedBy = $(this).attr('aria-describedby');
        const charCountElement = $('#' + ariaDescribedBy);
        const currentLength = $(this).val().length;
        charCountElement.text(`Entered: ${currentLength} characters.`);
    });

    // Adds light yellow on form focus fields
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

    // submiting business details for registration
    $('.register-bs-btn').click(function (e) {
        e.preventDefault();

        $(this).text("Processing...");

        // if required fields are missing show error
        isValid = true;
        $('.form-business, .form-owner').find(
            'input[required], textarea[required], select[required]').each(
            function(){
            if ($(this).val() == ''){
                isValid = false;
                $(this).addClass('is-invalid')
            } else{
                $(this).removeClass('is-invalid')
            }
        })

        function showAlert(message, type) {
            $('#flash-form-error').addClass(type).text(message).show();
        }

        // if missing fields return stop executing
        if (!isValid){
            showAlert('Please fill out all fields','error')
            $('.register-bs-btn').text("Submit");
            return;
        }

        //check if declarition was checked before submitting to server
        if ($('.declaration').find('input').is(':checked')) {
            let business_registration_data = {}
            let owner_info = {}
            let rawBusinessFormData = $('.form-business').serializeArray();
            let rawOwnerFormData = $('.form-owner').serializeArray();

            // retrieve business info from form object to be sent to the server
            $.each(rawBusinessFormData, function (index, obj) {
                business_registration_data[obj.name] = obj.value;
            });

            // retrieve owner info from form object to be sent to server
            $.each(rawOwnerFormData, function (index, obj) {
                owner_info[obj.name] = obj.value;
            });

            // send business info to the server
            $.ajax({
                url: "http://localhost:5003/api/v1/businesses",
                type: "POST",
                data: JSON.stringify(business_registration_data),
                contentType: "application/json",
                success: function (data) {
                    if (ownerInfoSubmitted) {
                        ownerInfoSubmitted = true;
                        window.location.href = "/dashboard";
                    }
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    showAlert('Something went wrong!', 'error')
                    $('.register-bs-btn').text("Submit");;
                }
            });

            // retrieve owner info from form object to be sent to the server
            let user_id = owner_info['owner']
            delete owner_info['owner'];

            // send owner info to the server
            $.ajax({
                url: "http://localhost:5003/api/v1/users/" + user_id,
                type: "PUT",
                data: JSON.stringify(owner_info),
                contentType: "application/json",
                success: function (data) {
                    if (businessInfoSubmitted) {
                        businessInfoSubmitted = true;
                        window.location.href = "/dashboard";
                    }
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    showAlert("Something went wrong!", 'error');
                    $('.register-bs-btn').text("Submit");
                }
            });
        } else {
            showAlert("Please accept the declaration to proceed.", 'error');
            $('.register-bs-btn').text("Submit");
        }
    });


// small screens js
    if ($(window).width() <= 768) {
        $('.menu').on('click', function () {
            let sideNav = $('.side-nav');
            if (sideNav.css('width') === '0px') {
                sideNav.css({
                    'width': '60%',
                    'transition': 'width 0.5s ease'
                });
            } else {
                sideNav.css({
                    'width': '0',
                    'transition': 'width 0.5s ease'
                });
            }
        });

        $(window).on('click', function (e) {
            // Check if the click is outside of the menu and the side-nav
            if (!$(e.target).closest('.menu').length && !$(e.target).closest('.side-nav').length) {
                $('.side-nav').css({
                    'width': '0',
                    'transition': 'width 0.5s ease'
                });
            }
        });
    }



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
