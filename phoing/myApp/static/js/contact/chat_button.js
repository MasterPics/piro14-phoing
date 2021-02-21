//Save
const onClickToPendings = async (contact_pk, request_user_pk) => {

    console.log("here1")
    try {
        console.log("here2")
        const options = {
            url: '/chat/add/',
            method: 'POST',
            data: {
                contact_pk: contact_pk, 
                request_user_pk: request_user_pk,
                csrfmiddlewaretoken: csrf_token, 
            }
        }
        console.log("here3")
        const response = await axios(options)
        console.log("here4")
        const responseOK = response && response.status === 200 && response.statusText === 'OK'
        // const responseOK = response && response.status === 200
        if (responseOK) {
            const data = response.data
            console.log("here5")
            modifyJoinToPending(data.contact_pk)
        }
    } catch (error ) {
        console.log(error)
    }

}

const modifyJoinToPending = async (contact_pk) => {
    console.log("here4")
    const btn = document.querySelector(`.chat-btn-${contact_pk} button`);
    btn.innerText = 'Pending'
}
