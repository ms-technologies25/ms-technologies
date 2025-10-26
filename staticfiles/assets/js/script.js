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
            window.location.href = '/contact';
        }
    }

    // Function to scroll to services section
    function scrollToServices() {
        const servicesSection = document.getElementById('services');
        if (servicesSection) {
            servicesSection.scrollIntoView({ behavior: 'smooth' });
        } else {
            // Fallback to category section if services doesn't exist
            const categorySection = document.getElementById('category');
            if (categorySection) {
                categorySection.scrollIntoView({ behavior: 'smooth' });
            }
        }
    }

    // Make functions globally available
    window.scrollToContact = scrollToContact;
    window.scrollToServices = scrollToServices;

    /*----------------------------------------- FAQ -----------------------------------------*/

    // FAQ toggle functionality
    function toggleFAQ(element) {
        const faqItem = element.parentElement;
        const isActive = faqItem.classList.contains('active');
        
        // Close all other FAQ items
        document.querySelectorAll('.faq-item').forEach(item => {
            item.classList.remove('active');
        });
        
        // Toggle current FAQ item
        if (!isActive) {
            faqItem.classList.add('active');
        }
    }

    // Make toggleFAQ globally available
    window.toggleFAQ = toggleFAQ;

    const menuIcon = document.querySelector('.nav-menu-icon');
    const navMenu = document.getElementById('nav-menu');
    const removeMenuButton = document.querySelector('.nav-menu-remove');
  
    menuIcon.addEventListener('click', function() {
      navMenu.classList.toggle('open');
    });
  
    removeMenuButton.addEventListener('click', function() {
      navMenu.classList.remove('open');
    });

    

    /*----------------------------------------- services -----------------------------------------*/

    // Add hover effects for service cards
    document.querySelectorAll('.service-card').forEach((card) => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-10px)';
        });
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
        });
    });

    // Add scroll animation for services section
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const servicesObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe service cards for animation
    document.querySelectorAll('.service-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        servicesObserver.observe(card);
    });
    
    /*----------------------------------------- search panel-----------------------------------------*/

    document.getElementById("search-icon").addEventListener("click", function () {
        document.getElementById("search-panel").classList.toggle("search-open");
    });

    document.getElementById("search-menu-icon").addEventListener("click", function () {
        document.getElementById("search-panel").classList.toggle("search-open");
        navMenu.classList.remove('open');
    });
    
    document.getElementById("search-close").addEventListener("click", function () {
        document.getElementById("search-panel").classList.remove("search-open");
    });


    /*----------------------------------------- searching functionality -----------------------------------------*/

    document.querySelector(".search-bar form").addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent form submission
        const searchQuery = document.querySelector("input[name='search']").value;
    
        fetch(`/?search=${encodeURIComponent(searchQuery)}`, {
            headers: { "X-Requested-With": "XMLHttpRequest" },
        })
        .then(response => response.json())
        .then(data => {
            const container = document.querySelector(".search-category-container");
            container.innerHTML = "";
    
            if (data.results.length === 0) {
                container.innerHTML = `<div class="no-results" style="font-style: italic">No products found for "${searchQuery}".</div>`;
            } 
            else {
                data.results.forEach(item => {
                    const productHTML = `
                        <div class="search-category-item">
                            <a href="/shop/product-details/${item.id}/">
                                <img src="${item.product_image_url}">
                                <div class="search-overlay">${item.product_name}<br> $${item.product_price}</div>
                            </a>
                        </div>`;
                    container.innerHTML += productHTML;
                });
            }
        });
    });

});

/*----------------------------------------- arrivals -----------------------------------------*/


document.querySelectorAll('.arrivals-product').forEach((item, index)=>{
    item.addEventListener('mouseenter', () => {
        item.style.transform = 'scale(1.02)';
    });
    item.addEventListener('mouseleave', () => {
        item.style.transform = 'scale(1)';
    });
});

const swiper = new Swiper('.arrivals-wrapper', {

    loop: true,
    grabCursor: true,
    spaceBetween: 15,

    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },

    breakpoints:{
        0:{
            slidesPerView: 1,
        },
        768:{
            slidesPerView: 2,
        },
        1025:{
            slidesPerView: 4,
        },
        1200:{
            slidesPerView: 5,
        },
        1600:{
            slidesPerView: 6,
        },
        2000:{
            slidesPerView: 7,
        },
        2400:{
            slidesPerView: 8,
        },
        2800:{
            slidesPerView: 9,
        },
    }
});

/*----------------------------------------- load products -----------------------------------------*/

document.addEventListener("DOMContentLoaded", function () {
    const products = document.querySelectorAll(".shop-product");
    const seeMoreBtn = document.getElementById("seeMoreBtn");
    const seeLessBtn = document.getElementById("seeLessBtn");
  
    let visibleCount = 20;
  
    const showProducts = () => {
      products.forEach((product, index) => {
        product.style.display = index < visibleCount ? "block" : "none";
      });
    };
  
    // Initial check to show or hide the See More button
    if (products.length > 20) {
      seeMoreBtn.style.display = "inline-block";
    } else {
      seeMoreBtn.style.display = "none";
    }
  
    seeMoreBtn.addEventListener("click", () => {
      visibleCount += 20;
      showProducts();
      seeLessBtn.style.display = "inline-block";
  
      if (visibleCount >= products.length) {
        seeMoreBtn.style.display = "none";
      }
    });
  
    seeLessBtn.addEventListener("click", () => {
      visibleCount = Math.max(20, visibleCount - 20);
      showProducts();
      seeMoreBtn.style.display = "inline-block";
  
      if (visibleCount === 20) {
        seeLessBtn.style.display = "none";
      }
    });
  
    // Initial rendering of products
    showProducts();
});
  