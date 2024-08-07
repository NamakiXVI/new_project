/* var socket = io.connect('https://' + document.domain + ':' + location.port);

socket.on('update_message_response', function(data) {
    console.log('works');
    var messagesDiv = document.getElementById('messages');
    var newMessage = document.createElement('p');
    newMessage.textContent = data.user + ': ' + data.content;
    messagesDiv.appendChild(newMessage);
});

function sendMessage(name) {
    var content = document.getElementById('content').value;
    socket.emit('update_message', { user: name, content: content });
    document.getElementById('content').value = '';
}

    <script src="{{url_for('static', filename='js-scripts/realtime-update-socketio.js')}}"></script> */
/*
$(document).ready(function() {
    function updateMessages() {
        // Make an AJAX request to get the latest message
        $.ajax({
            type: 'GET',
            url: '{{ url_for("start_page", name=name) }}',
            dataType: 'json',
            success: function(data) {
                if (data.message) {
                    // No new messages, do nothing
                } else {
                    // Update the page with the latest message
                    var message = data;
                    // Your logic to append the message to the chat window
                }
            },
            complete: function() {
                // Schedule the next update after a delay (e.g., 5 seconds)
                setTimeout(updateMessages, 1000);
            }
        });
    }

    // Start updating messages when the page loads
    updateMessages();
});
$(document).ready(function() {
    function updateMessages() {
        // Make an AJAX request to get the latest message
        $.ajax({
            type: 'GET',
            url: '{{ url_for("start_page", name=name) }}',
            dataType: 'json',
            success: function(data) {
                if (data.message) {
                    // No new messages, do nothing
                } else {
                    // Update the page with the latest message
                    var message = data;

                    // Append the new message to the chat window
                    var messageHTML = '<span class="d-flex ';
                    messageHTML += (name == message.user) ? 'justify-content-end' : 'justify-content-start';
                    messageHTML += ' mt-1">' + message.user + '</span>';
                    messageHTML += '<div class="d-flex ';
                    messageHTML += (name == message.user) ? 'justify-content-end' : 'justify-content-start';
                    messageHTML += '">';
                    messageHTML += '<div class="msg_box_div ';
                    messageHTML += (name == message.user) ? 'other_msg_color' : 'user_msg_color';
                    messageHTML += '"><div class="';
                    messageHTML += (' joined the chat' in message.content) ? 'on_join' : '';
                    messageHTML += '" style="padding: 3px 8px;">' + message.content + '</div></div></div>';
                    messageHTML += '<div class="d-flex ';
                    messageHTML += (name == message.user) ? 'justify-content-end' : 'justify-content-start';
                    messageHTML += '"><span class="msg_date">' + message.creation_date + '</span></div>';

                    // Append the HTML to the chat window
                    $('#chat-msg').append(messageHTML);
                }
            },
            complete: function() {
                // Schedule the next update after a delay (e.g., 5 seconds)
                setTimeout(updateMessages, 5000);
            }
        });
    }

    // Start updating messages when the page loads
    updateMessages();
});

*/

function alleZehnSekundenNeuLaden() {
  setInterval(function() {
    location.reload();
  }, 20000);
}

alleZehnSekundenNeuLaden();