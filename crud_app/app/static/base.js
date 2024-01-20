function setup() {
    const ajaxForms = $('form').filter(function () {
        return $(this).attr("action") !== undefined;
    });

    ajaxForms.on('submit', function (e) {
        e.preventDefault();
        handleAjaxSubmit($(this));
    });

    ajaxForms.filter(function () {
        return $(this).data('show-response-modal');
    }).on('submit-success', function (e, data) {
        renderResponsePopup($('#success-modal'), data);
    }).on('submit-failure', function (e, data) {
        renderResponsePopup($('#failure-modal'), data);
    });

    $('tr[data-href]').on("click", function () {
        window.location.href = $(this).data('href');
    });

    $('.delete-post').on('click', function (e) {
        $('#login-form').attr('action', $(this).data('url'));
        $('#login-form-title').text('Confirm credentials to delete post');
        $('#form-update-inputs').hide();
        $('#login-modal').modal('show');
    });

    $('.update-post').on('click', function (e) {
        $('#login-form').attr('action', $(this).data('url'));
        $('#login-form-title').text('Update Post');

        const formUpdateInputs = $('#form-update-inputs');
        const post = $(this).closest('.post');
        const postTitle = post.find('.post-title').text().trim();
        const postContent = post.find('.post-content').text().trim();

        formUpdateInputs.show();
        formUpdateInputs.find('#title').val(postTitle);
        formUpdateInputs.find('#content').val(postContent);

        $('#login-modal').modal('show');
    });

    $('#login-form').on('submit-success', function (e, data) {
        const post = $(`[data-post-id="${data.post_id}"]`);

        if (data.action === 'delete')
            post.remove();
        if (data.action === 'update') {
            post.find('.post-title').text(data.title);
            post.find('.post-content').text(data.content);
        }

        $('#login-modal').modal('hide');
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