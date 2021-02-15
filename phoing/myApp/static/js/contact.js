    var infinite = new Waypoint.Infinite({
        element: $('.infinite-container')[0],
        onBeforePageLoad: function () {
            $('.loading').show();
        },
        onAfterPageLoad: function ($items) {
            $('.loading').hide();
        }
    });

    //Save
    const onClickSave = async (contact_id) => {
        try {
            // const url = '/contact/';
            // const {
            //     data
            // } = await axios.post(url, {
            //     contact_id,
            // })
            // modify(data.contact_id, data.is_saved)

            const options = {
                url: '/contact/save/',
                method: 'POST',
                data: {
                    contact_id: contact_id,
                }
            }
            const response = await axios(options)
            const responseOK = response && response.status === 200 && response.statusText === 'OK'
            if (responseOK) {
                const data = response.data
                //modify에서는 이미 뒤집힌 is_saved 값이 들어감!
                modify(data.contact_id, data.is_saved)
            }
        } catch (error) {
            console.log(error)
        }
    }

    const modify = (contact_id, is_saved) => {
        const save = document.querySelector(`.save-${contact_id} i`);
        const save_content = document.querySelector(`.save-${contact_id} .save__content`)
        const num = save_content.innerText; // [ {{ contact.save_users.count }} ]
        console.log(num)
        if (is_saved === true) {

            save.className = "fas fa-bookmark";

            const count = Number(num) + 1;
            save_content.innerHTML = count
        } else {
            save.className = "far fa-bookmark";

            const count = Number(num) - 1;
            save_content.innerHTML = count
        }

    }
    //category
    const onClickLink = (category) => {
        const categoryIdInput = document.querySelector('#category')
        categoryIdInput.value = category
        const searchForm = document.querySelector('#searchForm')
        searchForm.submit()
    }

    //search
    const searchButton = document.querySelector('.btn_search')
    searchButton.addEventListener('click', () => {
        const searchClassInput = document.querySelector('.search')
        const searchIdInput = document.querySelector('#search')
        const searchForm = document.querySelector('#searchForm')
        searchIdInput.value = searchClassInput.value
        searchForm.submit()
    })


    //sort
    const sortClassInput = document.querySelector('.sort')
    sortClassInput.addEventListener('input', (e) => {
        const sortIdInput = document.querySelector('#sort')
        const searchForm = document.querySelector('#searchForm')
        sortIdInput.value = e.target.value
        searchForm.submit()
    })
