document.addEventListener("DOMContentLoaded", function (){

    /*----------------------------------------- header -----------------------------------------*/

    window.addEventListener('scroll', function(){
        const header = document.querySelector('header');

        if (window.scrollY > 0) header.classList.add('scrolled');
        else header.classList.remove('scrolled');
    });

    /*----------------------------------------- banner functions -----------------------------------------*/

    // Function to scroll to contact section
    function scrollToContact() {
        const contactSection = document.getElementById('contact');
        if (contactSection) {
            contactSection.scrollIntoView({ behavior: 'smooth' });
        } else {
            // If contact section doesn't exist, redirect to contact page
            window.location.href = '/contact/';
        }
    }

    // Function to scroll to services section
    function scrollToServices() {
        const servicesSection = document.getElementById('category');
        if (servicesSection) {
            servicesSection.scrollIntoView({ behavior: 'smooth' });
        }
    }

    // Make functions globally available
    window.scrollToContact = scrollToContact;
    window.scrollToServices = scrollToServices;

    const menuIcon = document.querySelector('.nav-menu-icon');
    const navMenu = document.getElementById('nav-menu');
    const removeMenuButton = document.querySelector('.nav-menu-remove');
  
    menuIcon.addEventListener('click', function() {
      navMenu.classList.toggle('open');
    });
  
    removeMenuButton.addEventListener('click', function() {
      navMenu.classList.remove('open');
    });
});