function message_popup(response){
    $('#message-success').show().html(response).fadeOut(2500, function () {});
}

function ajaxModal(form, url, error_mes) {
    $.ajax({
            type: 'POST',
            url: url,
            data: form.serialize(),
            dataType: 'json',
            success: function (response) {
                error_mes.html('');
                if ('errors' in response){
                    for (let n in response.errors){
                        error_mes.append(response.errors[n]);
                    }
                }
                else{
                    form.trigger('reset');
                    $('.modal').modal('hide');
                    message_popup(response.success_message);
                }
            }
        });
}

function poll(){
        $.ajax({url: "/update_user_info/",
                success: function(response){
                    let counter = $('.navbar-message-counter');
                    let sub_counter = $('.navbar-subscription-counter');
                    let total_new_comments = 0;

                    if (response.unread_messages != 0){

                        counter.html(response.unread_messages);
                    }

                    let subscriptions = $.parseJSON(response.subscriptions);
                    for (const key of Object.keys(subscriptions)) {
                        total_new_comments += parseInt(subscriptions[key]);
                        $('.dropdown-menu').find('a[href$="/article/' + key + '"]').find('span').html('(' + subscriptions[key] + ')');
                        }
                    sub_counter.html(total_new_comments);
                    $('#user-rating').html(response.user_rating);

                    let update_markers = [[counter, response.unread_messages], [sub_counter, total_new_comments]];

                    for (let i = 0; i < update_markers.length; i++ ) {
                        if (update_markers[i][1] != 0) {
                            update_markers[i][0].css('background-color', '#d90000');
                        }
                    }

                },
                dataType: "json",
                complete: setTimeout(function() {poll()}, 5000),
                timeout: 2000 });
    }


$(window).load(function () {
    (function check_user() {
        $.ajax({url: '/check_auth/',
                success: function (response) {
                    if (response.auth === 'true'){
                        return poll();
                    }
                }})
    })();

    $('.user-info-block button').click(function (e) {
        e.preventDefault();
        let url = '/block_user/' + window.location.pathname.split('/')[1] + '/';
        $.ajax({url:url,
                type: 'GET',
                success: function (response) {
                    message_popup(response.success_message);
                    $('.user-info-block button').html(response.action);
                }})
    });

    $('.password-reset-subm').click(function (e) {
        e.preventDefault();
        let form = $('.password-reset-form');
        let url = '/password_change/';
        let error_mes = $('.password-change-error-messages');
        return ajaxModal(form, url, error_mes);
    });

    $('.password-reset-close').click(function () {
        $(this).parent().prev().prev().html('');
    });

    $('.login-subm').click(function (e) {
        e.preventDefault();
        let form = $('.login-form');
        let url = '/login/';
        let error_mes = $('.login-error-messages');
        return ajaxModal(form, url, error_mes);
    });

    $('.registration-subm').click(function (e) {
        e.preventDefault();
        let form = $('.registration-form');
        let url = '/registration/';
        let error_mes = $('.registration-error-messages');
        return ajaxModal(form, url, error_mes);
    });

    $('.send-message-subm').click(function (e) {
        e.preventDefault();
        let form = $('.send-message-form');
        let url = '/send_message/' + window.location.pathname.split('/')[1] + '/';
        let error_mes = $('.send-message-error-messages');
        return ajaxModal(form, url, error_mes);
    });

    autosize($('textarea'));

});
