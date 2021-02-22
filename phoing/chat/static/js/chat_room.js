let old_msg_page_count = 0;
let loc = window.location, new_uri;
if (loc.protocol === "https:") {
    new_uri = "wss://";
} else {
    new_uri = "ws://";
}

let chatSocket = new ReconnectingWebSocket(
    new_uri + window.location.host +
    '/ws/chat/' + roomName + '/');
    

chatSocket.onopen = function(e) {
    fetchGroups();
    fetchMessages(true);
    
}





// const chatSocket = new WebSocket(
//     'ws://'
//     + window.location.host
//     + '/ws/chat/'
//     + roomName
//     + '/'
// );

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    document.querySelector('#chat-log').value += (data.message + '\n');
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message
    }));
    messageInputDom.value = '';
};


function fetchGroups() {
    chatSocket.send(JSON.stringify({'command': 'fetch_groups','username' : username }));
  }