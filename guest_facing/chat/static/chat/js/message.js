var pubnubConfig = JSON.parse($('#pubnub-config').text() || '""')
    , guestUuid = pubnubConfig.uuid
    , systemOutTime = JSON.parse($('#system-out-time').text() || '""')
    , systemMessages = JSON.parse($('#system-messages').text() || '""');

pubnub = new PubNub({
    subscribeKey : pubnubConfig.subscribe_key || '',
    uuid: pubnubConfig.uuid || '',
});

$(document).ready(function() {
    $('body').addClass('live');

    pubnub.addListener({
        status: function(statusEvent) {
        },
        message: function(msgLoad) {
            if (msgLoad.channel == pubnubConfig.channel) {
                createMessageList(msgLoad.channel, msgLoad.publisher, msgLoad.message, msgLoad.timetoken);
            }
        },
        presence: function(presenceEvent) {
            // This is where you handle presence. Not important for now :)
        }
    });
    
    
    pubnub.subscribe({
        channels: [pubnubConfig.channel],
    });

    fetchMessages();
});


$('#form-message').submit(function() {
    event.preventDefault();
    if (!$('#id_message').val().trim()) {
        return;
    }
    var data = $(this).serializeArray();
    $('#id_message').val('');

    $.ajax({
        url: '/guest/chat/message/',
        data: data,
        type: 'POST',
        success: function(result) {
            if ((result.status || 'error') != 'success') {
                console.error('Error client: '+ error);
            }
        }, error: function(xhr, text, error) {
            console.error('Error client: '+ error);
        }
    });
});


function fetchMessages() {
    pubnub.fetchMessages(
        {
            channels: [pubnubConfig.channel],
            includeUUID: true,
            // includeMeta: true,
        },
        (status, response) => {
            if (status.statusCode == 200) {
                $.each(response.channels, function(channel, messages) {
                    $.each(messages, function(index, msgLoad) {
                        if (channel == pubnubConfig.channel) {
                            createMessageList(channel, msgLoad.uuid, msgLoad.message, msgLoad.timetoken)
                        }
                    });
                });

                // system message out of time
                if (systemOutTime) {
                    createSystemOutTime();
                }
            } else {
                console.error("Operation failed w/ error:", status);
            }
        }
    );
}


function createMessageList(channel, msgUuid, msgText, msgTimetoken) {
    var $msg;

    if (msgUuid != guestUuid) {
        $msg = $(
            '<div class="message people">'+
                '<div class="chat-card bg-primary text-primary-reverse">'+
                    '<div class="card-text">'+
                        '<div class="chat-body">'+ msgText +'</div>'+
                        '<div class="text-10">'+ convertTimetoken(msgTimetoken) +'</div>'+
                    '</div>'+
                '</div>'+
            '</div>');
    } else {
        $msg = $(
            '<div class="message self">'+
                '<div class="chat-card bg-light text-light-reverse">'+
                    '<div class="card-text">'+
                        '<div class="chat-body">'+ msgText +'</div>'+
                        '<div class="text-10">'+ convertTimetoken(msgTimetoken) +'</div>'+
                    '</div>'+
                '</div>'+
            '</div>');
    }
    $('#messages').append($msg);
    $('#messages').scrollTop($('#messages').prop('scrollHeight'));
}


function convertTimetoken(timetoken) {
    // return timetoken;
    if (!timetoken) {
        return '';
    }
    var date = new Date(timetoken / 1e4); // 1e4 = 10000
    return date.getDate() +'/'+ (date.getMonth() + 1) +'/'+ date.getFullYear() +' '+ date.getHours() +':'+ date.getMinutes()
}


function createSystemOutTime() {
    var $msg = $(
            '<div class="message system">'+
                '<div class="chat-card bg-info text-info-reverse">'+
                    '<div class="card-text">'+
                        '<div class="chat-body">'+ systemMessages.out_time +'</div>'+
                    '</div>'+
                '</div>'+
            '</div>'
        );
    $('#messages').append($msg);
    $('#messages').scrollTop($('#messages').prop('scrollHeight'));
}
