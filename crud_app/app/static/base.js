function setup() {
    $('form').filter(function () {
        return $(this).attr("action") !== undefined;
    }).on('submit', function (e) {
        e.preventDefault();
        handleAjaxSubmit($(this));
    }).filter(function () {
        return $(this).data('show-response-modal');
    }).on('submit-success', function (e, data) {
        console.log(data)
        renderResponsePopup($('#success-modal'), data);
    }).on('submit-failure', function (e, data) {
        renderResponsePopup($('#failure-modal'), data);
    });
}

function handleAjaxSubmit(form) {
    $.ajax({
        type: 'POST',
        url: form.attr('action'),
        data: form.serialize(),
        contentType: "application/x-www-form-urlencoded",
        success: function (data) {
            form.trigger('submit-complete', [data])

            if (data.status === 'success') {
                form.trigger('submit-success', [data]);
                form[0].reset();
            }
            else
                form.trigger('submit-failure', [data]);
        },
        error: function (error) {
            const data = {
                status: 'failure',
                message: error.responseText
            }

            form.trigger('submit-complete', [data])
            form.trigger('submit-failure', [data]);
        }
    });
}

function renderResponsePopup(popup, data) {
    popup.find('.modal-body .modal-message').text(data.message);
    popup.modal('show');
}