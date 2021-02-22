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
    // fetchGroup(); // get group info
    fetchMessages(true); // get messages
    }


chatSocket.onmessage = function(e) {
    var data = JSON.parse(e.data);
    if (data['command'] === 'messages') {

        var ChatLog = document.querySelector('.message-container');
        var elements = ChatLog.querySelectorAll('.comment');

        if (elements) {
            for (let i = 0; i < elements.length; i++){
                elements[i].parentNode.removeChild(elements[i])
            }
        }
        
        
        // while(elements){
        // elements[0].parentNode.removeChild(elements[0]);
        // }

        for (let i=0; i<data['messages'].length; i++) {
        createMessage(data['messages'][i]);
        }
        if(old_msg_page_count == 0){
        scroll();
        }

    } else if (data['command'] === 'new_message'){
        if(old_msg_page_count != 0){
        old_msg_page_count = 0;
        fetchMessages(true);
        }
        createMessage(data['message']);
        scroll();
    }
    // else if (data['command'] === 'groups'){
    //     for (let i=0; i<data['groups'].length; i++) {
    //     createGroup(data['groups'][i]);
    //     }
    // }
};

// const chatSocket = new WebSocket(
//     'ws://'
//     + window.location.host
//     + '/ws/chat/'
//     + roomName
//     + '/'
// );

// chatSocket.onmessage = function(e) {
//     const data = JSON.parse(e.data);
//     document.querySelector('#chat-log').value += (data.message + '\n');
// };

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('.textarea-container textarea').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('.send').click();
    }
};

document.querySelector('.send').onclick = function(e) {
    var messageInputDom = document.querySelector('.textarea-container textarea')
    var message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'command': 'new_message',
        'message': message,
        'from': username,
        'grp_name' : roomName
    }));

    messageInputDom.value = '';
    scroll();
};

document.querySelector('#check_older_messages').onclick = function(e) {
    old_msg_page_count++;
     fetchMessages(false);
  };

// document.querySelector('#chat-message-input').focus();
// document.querySelector('#chat-message-input').onkeyup = function(e) {
//     if (e.keyCode === 13) {  // enter, return
//         document.querySelector('#chat-message-submit').click();
//     }
// };

// document.querySelector('#chat-message-submit').onclick = function(e) {
//     const messageInputDom = document.querySelector('#chat-message-input');
//     const message = messageInputDom.value;
//     chatSocket.send(JSON.stringify({
//         'message': message
//     }));
//     messageInputDom.value = '';
// };


// STARTS HERE!

// function fetchGroup() {
//     chatSocket.send(JSON.stringify({'command': 'fetch_group','username' : username, 'room_name': roomName,  }));
// }


function fetchMessages(recent) {
    if(recent){
      chatSocket.send(JSON.stringify({'command': 'fetch_messages','room_name' : roomName }));  
    }
    chatSocket.send(JSON.stringify({'command': 'fetch_old_messages','room_name' : roomName }));
  }


  function convertToMonth(index){
    switch(index){
      case 1:
        return 'Jan'
      case 2:
        return 'Feb'
      case 3:
        return 'Mar'
      case 4:
        return 'Apr'
      case 5:
        return 'May'
      case 6:
        return 'Jun'
      case 7:
        return 'Jul'
      case 8:
        return 'Aug'
      case 9:
        return 'Sep'
      case 10:
        return 'Oct'
      case 11:
        return 'Nov'
      case 12:
        return 'Dec'
    }
  }



function formatDate(date) {
    var hours = date.getHours();
    var minutes = date.getMinutes();
    var ampm = hours >= 12 ? 'pm' : 'am';
    hours = hours % 12;
    hours = hours ? hours : 12; // the hour '0' should be '12'
    minutes = minutes < 10 ? '0'+minutes : minutes;
    var strTime = hours + ':' + minutes + ' ' + ampm;
    //return strTime;
    return date.getDate() + " " + convertToMonth(date.getMonth()+1) + "  " + strTime;
}


function createMessage(data) {
var author = data['author'];

// outermost
let commentDivTag = document.createElement('div');
// commentDivTag.classList.add('comment');


// middlel layer
let imgTag = document.createElement('img');
let nameDivTag = document.createElement('div');
nameDivTag.classList.add('name')
let bubbleDivTag = document.createElement('div');
bubbleDivTag.classList.add('bubble')


// innermost
let contentDivTag = document.createElement('div');
contentDivTag.classList.add('content');
let timestampDivTag = document.createElement('div');
timestampDivTag.classList.add('timestamp');


nameDivTag.textContent = author;
contentDivTag.textContent = data.content;

let date_posted = new Date(data.timestamp);
timestampDivTag.textContent = formatDate(date_posted);

imgTag.src = data["author_profile_img"];

if (author === username){
    commentDivTag.classList.add('me', 'comment')
} else {
    commentDivTag.classList.add('other', 'comment')
}

commentDivTag.append(imgTag);
commentDivTag.append(author);
commentDivTag.append(bubbleDivTag);
bubbleDivTag.append(contentDivTag);
bubbleDivTag.append(timestampDivTag);

document.querySelector('.message-container').appendChild(commentDivTag);


}

