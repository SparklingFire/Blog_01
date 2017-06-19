function messageBuilder(response) {

}

$(document).ready(function () {
    let checked = [];


    $(document).on('click', '.send-message-popover',function (e) {
       e.preventDefault();
       let target_user = $(this).closest('.media').find('.comment-author-username').attr('data-id');
       let send_message = $('#SendMessage');
       send_message.find('.modal-target-username').html(target_user);
       send_message.modal().draggable();
   });

    $(document).on('click', '.password-reset-submit', function (e) {
        e.preventDefault();
        let form = $('.password-reset-form');
        $.ajax({
            type: 'POST',
            dataType: 'json',
            data: form.serialize(),
            url: '/password_change/',
            success: function (response) {
                $('#password-change').modal('toggle');
            },
            error: function (xhr, errmsg, err) {
                    alert(xhr.status + ": " + xhr.responseText);
            }
        })
    });

    let marker = '.filter-' + $(location).attr('pathname').match(/[a-z]+/gi)[2];
    $(marker).css({'background-color':'#717171', 'color': 'white'});

    $('.pagination li').on('click', function (e) {
        let page = $(this).data('page');
        let url = '/message_list/all/?page=' + page;
        e.preventDefault();
        $.ajax({
            method: 'GET',
            dataType: 'json',
            url: url,
            success: function (response) {
                let messages_list_table = $('.messages-list-table');
                messages_list_table.hide();
                $('.messages-list-message').remove();
                response.forEach(function (response) {
                   $('.messages-list-table').append(messageBuilder(response));
                });
                messages_list_table.show();
                window.history.pushState("object or string", "Title", url);
            }
        })
    });

    $('.message-checkbox').on('click', function (e) {
        let checkbox_id = $(this).attr('data-id');

        if ($(this).is(':checked')){
            checked.push(checkbox_id);
        }
        else{
            checked.splice(checked.indexOf(checkbox_id), 1);
        }

    });

        $('.messages-list-message').mouseenter(function () {
        $(this).css('cursor', 'pointer');
        $(this).find('.messages-list-message-text-title').css('color', '#cc181e');
        $(this).find('.messages-list-message-user-info').css('color', '#cc181e');
    });

    $('.messages-list-message').mouseleave(function () {
        $(this).find('.messages-list-message-text-title').css('color', '#1a1a1a');
        $(this).find('.messages-list-message-user-info').css('color', '#1a1a1a');

    })
});
