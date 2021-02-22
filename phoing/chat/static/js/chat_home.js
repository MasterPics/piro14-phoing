//Save


const onClickToMembers = async (contact_pk, request_user_pk) => {

    try {
        const options = {
            url: '/chat/member/',
            method: 'POST',
            data: {
                contact_pk: contact_pk, 
                request_user_pk: request_user_pk,
            }
        }
        const response = await axios(options)
        const responseOK = response && response.status === 200 && response.statusText === 'OK'
        // const responseOK = response && response.status === 200
        if (responseOK) {
            const data = response.data
            modifyPendingToMember(data.contact_pk, data.member_pk, data.member_username, data.member_category)
        }
    } catch (error ) {
        console.log(error)
    }
}

const onClickToReject = async (contact_pk, request_user_pk) => {

    try {
        const options = {
            url: '/chat/reject/',
            method: 'POST',
            data: {
                contact_pk: contact_pk, 
                request_user_pk: request_user_pk,
            }
        }
        const response = await axios(options)
        const responseOK = response && response.status === 200 && response.statusText === 'OK'
        // const responseOK = response && response.status === 200
        if (responseOK) {
            const data = response.data
            modifyPendingToReject(data.contact_pk, data.member_pk)
        }
    } catch (error ) {
        console.log(error)
    }
}

const modifyPendingToMember = async (contact_pk, member_pk, member_username, member_category) => {

        const pendingDiv = document.querySelector(`.profile-right-${contact_pk} .member-${member_pk}`);
        pendingDiv.remove()

        const parentDiv = document.querySelector(`.profile-right-${contact_pk} .profile-members`)
        const memberDivOuter = document.createElement('div');
        memberDivOuter.classList.add(`member`, `member-${member_pk}`);
        const memberDivInner = document.createElement('div');
        memberDivInner.classList.add(`member-info-${member_pk}`, `member-info`);
        memberDivInner.innerHTML = `${member_username} <span class="middot"> &middot;</span> <span class="member-category">${ member_category }</span>`
        memberDivOuter.appendChild(memberDivInner)
        parentDiv.appendChild(memberDivOuter)
        
    
    }

const modifyPendingToReject = async (contact_pk, member_pk) => {
    const pendingDiv = document.querySelector(`.profile-right-${contact_pk} .member-${member_pk}`);
        pendingDiv.remove()
}

// const onClickToMembers = async (contact_pk, request_user_pk) => {
//     const url = "/chat/member/";
    
//     const {data} = await axios.post(url, {
//         contact_pk: contact_pk,
//         request_user_pk:request_user_pk,
//     })
    
//     modifyJoinToPending(data.contact_pk);
    
// }

// const modifyPendingToMember

// const onClickToMembers = async (contact_pk, request_user_pk) => {
//     const url = "/chat/reject/";
    
//     const {data} = await axios.post(url, {
//         contact_pk: contact_pk,
//         request_user_pk:request_user_pk,
//     })
    
//     modifyJoinToPending(data.contact_pk);
    
// }

// const modifyJoinToPending = async (contact_pk) => {
//     console.log("here4")
//     const btn = document.querySelector(`.chat-btn-${contact_pk} button`);
//     btn.innerText = 'Requested'
// }




// const onClickToPendings = async (contact_pk, request_user_pk) => {

//     console.log("here1")
//     try {
//         console.log("here2")
//         const options = {
//             url: '/chat/add/',
//             method: 'POST',
//             data: {
//                 contact_pk: contact_pk, 
//                 request_user_pk: request_user_pk,
//                 csrfmiddlewaretoken: csrf_token, 
//             }
//         }
//         console.log("here3")
//         const response = await axios(options)
//         console.log("here4")
//         const responseOK = response && response.status === 200 && response.statusText === 'OK'
//         // const responseOK = response && response.status === 200
//         if (responseOK) {
//             const data = response.data
//             console.log("here5")
//             modifyJoinToPending(data.contact_pk)
//         }
//     } catch (error ) {
//         console.log(error)
//     }

// }

// const modifyJoinToPending = async (contact_pk) => {
//     console.log("here4")
//     const btn = document.querySelector(`.chat-btn-${contact_pk} button`);
//     btn.innerText = 'Requested'
// }






// const modify = (id, like) => {
// const heart = document.querySelector(`.like-${id} i`);
// const like_con = document.querySelector(`.like-${id} .like__content`);

// if (like === false) {
//     heart.className = "far fa-heart";
//     like_con.innerHTML = "게시물이 마음에 드시면 좋아요를 눌러주세요!";
// }
// else {
//     heart.className = "fas fa-heart";
//     like_con.innerHTML = "이 게시물에 좋아요를 누르셨습니다!";
// }
// }