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
        $('#flash-message, #flash-error-p').fadeOut('slow', function () {
            $(this).hide();
        });
    }, 8000);
    // ------------------------------------------------------------------------

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
        let isValid = true;
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

        // if missing fields return stop executing
        if (!isValid){
            showAlert('Please fill out all fields', 'error', 'flash-form-error')
            fadeOut('flash-msg')
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

            let ownerInfoSubmitted = false;
            let businessInfoSubmitted = false;
            // send business info to the server
            $.ajax({
                url: "https://www.epermit.live/api/v1/businesses",
                type: "POST",
                data: JSON.stringify(business_registration_data),
                contentType: "application/json",
                success: function (data) {
                    businessInfoSubmitted = true;
                    if (ownerInfoSubmitted) {
                        $('.register-bs-btn').text("Submit");
                        showAlert("Successfully submited!!", 'success', 'flash-form-error');
                        fadeOut('.flash-msg')
                        window.location.href = "https://www.epermit.live/dashboard";
                    }
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    showAlert('Something went wrong!', 'error', 'flash-form-error')
                    fadeOut('flash-msg')
                    $('.register-bs-btn').text("Submit");
                }
            });

            // // retrieve owner info from form object to be sent to the server
            let user_id = owner_info['owner']
            delete owner_info['owner'];

            // send owner info to the server
            $.ajax({
                url: "https://www.epermit.live/api/v1/users/" + user_id,
                type: "PUT",
                data: JSON.stringify(owner_info),
                contentType: "application/json",
                success: function (data) {
                    ownerInfoSubmitted = true;
                    if (businessInfoSubmitted) {
                        $('.register-bs-btn').text("Submit");
                        showAlert("Successfully submited!!", 'success', 'flash-form-error');
                        fadeOut('flash-msg')
                        window.location.href = "https://www.epermit.live/dashboard";
                    }
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    showAlert("Something went wrong!", 'error', 'flash-form-error');
                    fadeOut('flash-msg');
                    $('.register-bs-btn').text("Submit");
                }
            });
        } else {
            showAlert("Please accept the declaration to proceed.", 'error', 'flash-form-error');
            fadeOut('flash-msg');
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

    // Permit payement
    $('#pay-permit').on('click', function(e){
        e.preventDefault()
        let isValid = true;
        mpesaForm = $('#mpesa-form')
        errorMsgDiv = $('.error-p-f')

        mpesaForm.find('input[required], select[required]').each(
                function () {
                    if ($(this).val() == '') {
                        isValid = false;
                        $(this).addClass('is-invalid')
                    } else {
                        $(this).removeClass('is-invalid')
                    }
                })

        // if missing fields return stop executing
        if (!isValid) {
            showAlert('Please fill out all fields', 'error', 'flash-error-p')
            fadeOut('error-p-f')
            $('.register-bs-btn').text("Submit");
            return;
        }

        let businessDataReqPermit = {}
        let mpesaFormRawData = mpesaForm.serializeArray();

        // retrieve business info from form object to be sent to the server
        $.each(mpesaFormRawData, function (index, obj) {
            businessDataReqPermit[obj.name] = obj.value;
        });
        console.log(businessDataReqPermit)

        resultCode  = stkPush(businessDataReqPermit)
    })
});
// -------------------------------- End of document ready -------------------------------------------

// This function fades out an element after a given time.
function fadeOut(className, timeInSec=8000) {
    setTimeout(function () {
        $('.' + className).fadeOut('slow', function () {
            $(this).hide();
            if ($(this).hasClass('error')) {
                $(this).removeClass('error');
            }else if ($(this).hasClass('success')) {
                $(this).removeClass('success');
            }
            $(this).text('');
        });
    }, timeInSec);
}

// This function shows an alert message
function showAlert(message, type, id) {
    $('#' + id).addClass(type).text(message).css({ 'padding-top': '18px' }).show();
}

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
            position: e.latLng,
            map: map,
            title: "Clicked Location",
        });
    });
}


// STK push
function stkPush(businessDataReqPermit){
    $.ajax({
        url: 'https://www.epermit.live/api/v1/paympesa',
        type: 'POST',
        data: JSON.stringify(businessDataReqPermit),
        contentType: "application/json",
        success: function (data) {
            showAlert('Payment request sent, Please check your phone.', 'success', 'flash-error-p');
            fadeOut('error-p-f', 10000);

           // give client 15sec before checking payment status
            setTimeout(function () {
                stkQuery(businessDataReqPermit['business_id']);
            }, 15000);
        },
        error: function (data) {
            console.error('Error sending STK push request.');
            showAlert('An error occurred. Please try again.', 'error', 'flash-error-p');
        }

    })

// stk query
function stkQuery(business_id) {
    $.ajax({
        url: 'https://www.epermit.live/api/v1/stkquery',
        type: 'GET',
        success: function (data) {
            errorCode = data['errorCode'];
            if (errorCode){
                showAlert('An error occurred while processing. Please try again later.', 'error', 'flash-error-p');
                fadeOut('error-p-f');
            }else{
                console.log(data);
                const resultCode = data['ResultCode'];
                console.log(resultCode)
                handlePaymentStatus(resultCode, business_id);
            }
        },
        error: function () {
            console.log('Error querying payment status.');
        }
    });
}}

// This function handles the payment status
function handlePaymentStatus(resultCode, business_id) {
    if (resultCode === '0') {
        showAlert('Payment was successful!', 'success', 'flash-error-p');
        fadeOut('error-p-f');
        window.location.href = "https://www.epermit.live/pdf";

    } else if (resultCode === '1032') {
        showAlert('The payment request was canceled.', 'error', 'flash-error-p');
        fadeOut('error-p-f');
        window.location.href = "https://www.epermit.live/pdf";
        getPermit(business_id)
    } else {
        showAlert('An error occurred while processing payment. Please try again later.', 'error', 'flash-error-p');
        fadeOut('error-p-f');
    }}

// This functions gets permit
function getPermit(business_id){
    console.log(business_id)
    $.ajax({
        url: 'https://www.epermit.live/api/v1/generatepermit/'+ business_id,
        type: 'GET',
        xhrFields: {
            responseType: 'blob'
        },
        success: function (data) {
            console.log(data)
            $('#loading').hide();
            $('#generatePermitBtn').prop('disabled', false);
            const url = window.URL.createObjectURL(data);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = 'permit.pdf';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            $('#message').text('Permit generated successfully.').addClass('text-success');
        },
        error: function (data) {
            console.log('Error getting permit')
            $('#loading').hide();
            $('#generatePermitBtn').prop('disabled', false);
            $('#message').text('Error getting permit').addClass('text-danger');
        }
    })
}