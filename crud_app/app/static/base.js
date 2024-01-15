function setup() {
    $('form').filter(function () {
        return $(this).attr("action") !== undefined;
    }).on('submit', function (e) {
        e.preventDefault();
        handleAjaxSubmit($(this));
    });
}

function handleAjaxSubmit(form) {
    $.ajax({
        type: 'POST',
        url: form.attr('action'),
        data: form.serialize(),
        success: function (data) {
            console.log(data)
            form[0].reset();

            form.trigger('submit-complete', [data])

            if (data.status === 'success')
                form.trigger('submit-success', [data]);
            else {
                form.trigger('submit-failure', [data]);

                if (data.status === 'invalid')
                    form.trigger('submit-invalid', [data])
                else if (data.status === 'impermissible')
                    form.trigger('submit-impermissible', [data])
                else if (data.status === 'error')
                    form.trigger('submit-error', [data])
            }
        }
    });
}
