$(document).ready(function () {
    $('#refresh-captcha').on('click', function () {
        const timestamp = Date.now();
        const newUrl = '/captcha_image?timestamp=' + timestamp;
        $.ajax({
            url: newUrl,
            method: 'GET',
            success: function (response, textStatus, jqXHR) {
                const contentType = jqXHR.getResponseHeader('Content-Type');
                if (contentType === 'image/png') {
                    $('#captcha-image').attr('src', newUrl);
                }
            },
            error: function () {
                console.error('Error fetching captcha image.');
            },
            processData: false,
            responseType: 'arraybuffer'
        });
    });
});