const toggleBtn = document.querySelector('.nav__toggleBtn');
const menu = document.querySelector('.nav__menu');
const profile = document.querySelector('.nav__profile');
toggleBtn.addEventListener('click', ()=>{
    menu.classList.toggle('active')
    profile.classList.toggle('active')
});