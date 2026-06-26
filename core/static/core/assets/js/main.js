// Atelier Aura — main.js
// Note: mobile menu and dropdown are handled inline in base.html
// This file is kept for any future global utilities

window.addEventListener('resize', () => {
  if (window.innerWidth > 900) {
    const navList = document.querySelector('.nav-list');
    const menuToggle = document.querySelector('.menu-toggle');
    if (navList) navList.classList.remove('active');
    if (menuToggle) menuToggle.classList.remove('active');
    document.body.classList.remove('menu-open');
    document.body.style.overflow = '';
  }
});
