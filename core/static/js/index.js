function onOpenModal(modal) {
    if (modal) {
        modal.style.display = "block"
    }
    document.body.style.margin = "0"
    document.body.style.overflow = "hidden"
    document.body.style.height = "100%"
}

function onCloseModal(modal) {
    if (modal) {
        modal.style.display = "none"
    }
    document.body.style.margin = "0"
    document.body.style.overflow = "unset"
    document.body.style.height = "unset"
}

const modals = document.querySelectorAll(".modal")

document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
        modals.forEach(modal => onCloseModal(modal))
    }
})

document.querySelectorAll(".modal__close").forEach(el => {
    el.addEventListener("click", function () {
        onCloseModal(el.closest(".modal"))
    })
})

const menuCloseBtn = document.querySelector(".menu-close");

menuCloseBtn?.addEventListener("click", function () {
    onCloseModal(menuCloseBtn.closest(".modal"))
})

document.querySelectorAll(".modal-overlay").forEach(modalOverlay => {
    modalOverlay.addEventListener("click", function (event) {
        onCloseModal(modalOverlay.closest(".modal"))
    })
})

document.querySelectorAll("[data-modal]").forEach(modalButton => {
    const modalId = modalButton.dataset.modal;
    const modal = document.querySelector(`.modal[id="${modalId}"]`)
    if (modal) {
        modalButton.addEventListener("click", () => {
            onOpenModal(modal)
            if (modal.id === "order") {
                let serviceName = modalButton.dataset.serviceName;
                let modalServiceTitle = modal.querySelector(".modal__service-name");
                let modalServiceInput = modal.querySelector('input[name="service"]')
                if (serviceName) {
                    if (modalServiceTitle) modalServiceTitle.innerText = serviceName
                    if (modalServiceInput) modalServiceInput.value = serviceName
                }
            }
        })
    }
})

function setCookie(name, value, days) {
    var expires = ""
    if (days) {
        var date = new Date()
        date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000)
        expires = "; expires=" + date.toUTCString()
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/"
}

function getCookie(name) {
    var nameEQ = name + "="
    var ca = document.cookie.split(";")
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i]
        while (c.charAt(0) == " ") c = c.substring(1, c.length)
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length)
    }
    return null
}

const cookieModal = document.querySelector(".modal-cookie")
const cookieBtn = document.querySelector(".modal-cookie__button")

if (!getCookie("utp_accept_cookies")) {
    cookieModal.classList.add("show")
    cookieBtn.addEventListener("click", cookieBtnClick)

    function cookieBtnClick() {
        cookieModal.classList.remove("show")
        setCookie("utp_accept_cookies", true)
    }
}

const btnUp = {
    el: document.querySelector(".up-arrow-btn"),
    show() {
        this.el.classList.remove("btn-up_hide")
    },
    hide() {
        this.el.classList.add("btn-up_hide")
    },
    addEventListener() {
        window.addEventListener("scroll", () => {
            const scrollY = window.scrollY || document.documentElement.scrollTop
            scrollY > 400 ? this.show() : this.hide()
        })
        document.querySelector(".up-arrow-btn").onclick = () => {
            window.scrollTo({
                top: 0,
                left: 0,
                behavior: "smooth",
            })
        }
    },
}
btnUp.addEventListener() // Make the DIV element draggable:

// Формы
document.querySelectorAll("form").forEach(form => {
    if (form.getAttribute("data-action")) {
        form.setAttribute("action", form.getAttribute("data-action"))
    }

    if (form.hasAttribute("data-ignore-fields")) return

    if (!form.querySelector('[name="csrfmiddlewaretoken"]')) {
        let csrfInput = document.createElement("input")
        csrfInput.setAttribute("name", "csrfmiddlewaretoken")
        csrfInput.setAttribute("value", window.securpb.csrfToken)
        csrfInput.setAttribute("type", "hidden")
        form.appendChild(csrfInput)
    }

    setFieldAttributes(form, "email", {
        maxlength: "100",
        pattern: "^([A-z0-9_-]+.)*[A-z0-9_-]+@[a-z0-9_-]+(.[a-z0-9_-]+)*.[a-z]{2,6}$",
    })

    setFieldAttributes(form, "phone", {
        maxlength: "21",
    })

    setFieldAttributes(form, "name", {
        maxlength: "100",
        pattern: "(^[a-zA-Zа-яА-ЯёЁ]+ ?[a-zA-Zа-яА-ЯёЁ]* ?[a-zA-Zа-яА-ЯёЁ]*)?$",
    })

    if (form.classList.contains("needs-validation")) {
        form.addEventListener("submit", event => {
            if (!form.checkValidity()) {
                event.preventDefault()
                event.stopPropagation()
            } else {
                event.preventDefault()
                submitForm(form)
            }
            form.classList.add("was-validated")
        })
    }
})

// Установка атбрибутов
function setFieldAttributes(form, fieldName, attributes) {
    let field = form.querySelector(`[name="${fieldName}"]`)
    if (field) {
        for (let attr in attributes) {
            field.setAttribute(attr, attributes[attr])
        }
    }
}

function maskPhone() {
    let t = document.querySelectorAll('input[name="phone"]')
    t.length &&
    t.forEach(t => {
        IMask(t, {
            mask: "+{7} (000) 000-00-00",
            prepare: function (t, r) {
                return "8" === t && "" === r.value ? "" : t
            },
        })
    })
}

maskPhone()

// Отправка формы
async function submitForm(form) {
    let formData = new FormData(form)
    formData.set("source", window.securpb.source)
    formData.set("refer", window.securpb.refer)
    let action = form.getAttribute("action") || form.getAttribute("data-action")
    try {
        let response = await fetch(action, {
            method: "POST",
            body: formData,
        })
        if (response.ok) {
            let result = await response.json()
            console.log("Форма успешно отправлена")

            modals.forEach(modal => onCloseModal(modal))

            let successModalId = "success"
            if (form.dataset.successModal) {
                successModalId = form.dataset.successModal
            }
            let successModal = document.getElementById(successModalId)
            if (successModal) {
                onOpenModal(successModal)
                setTimeout(() => {
                    onCloseModal(successModal)
                }, 2200);
            }

            form.reset()
            form.classList.remove("was-validated")

            if (form.hasAttribute("data-goal")) {
                try {
                    ym(window.securpb.ym_id, "reachGoal", form.getAttribute("data-goal"))
                } catch (error) {
                    console.error(error)
                }
            }
        } else {
            console.error("Ошибка при отправке формы")
        }
    } catch (error) {
        console.error(error)
    }
}


function setAutoplay(duration = 0) {
    if (!document.querySelector('.circle-progress__bar')) return;

    let circle = document.querySelector('.circle-progress__bar'),
        radius = circle.getAttribute('r'),
        cf = 2 * Math.PI * radius;

    circle.setAttribute('stroke-dasharray', `${cf} ${cf}`);
    start(duration);

    setInterval(() => {
        start(duration);
        facts.slideNext();
    }, duration);

    function start(duration) {
        const start = performance.now();

        requestAnimationFrame(animate);

        function animate(time) {
            let timeFraction = (time - start) / duration;

            if (timeFraction > 1) timeFraction = 1;

            setProgress(timeFraction * 100);

            if (timeFraction < 1) {
                requestAnimationFrame(animate);
            }
        }
    }

    function setProgress(percent) {
        circle.style.strokeDashoffset = cf - (percent / 100) * cf;
    }
}

const facts = new Swiper('.facts__slider', {
    loop: true,
    speed: 1000,
    watchSlidesProgress: true,
    mousewheelControl: true,
    keyboardControl: true,
    navigation: {
        prevEl: '.facts__prev',
        nextEl: '.facts__next',
    },
    on: {
        init() {
            setAutoplay(5000);
        },
        progress(swiper) {
            for (let i = 0; i < swiper.slides.length; i++) {
                const slideProgress = swiper.slides[i].progress;
                const innerOffset = swiper.width * interleaveOffset;
                const innerTranslate = slideProgress * innerOffset;

                swiper.slides[i].querySelector('.facts__item').style.transform = `translateX(${innerTranslate}px)`;
            }
        },
        touchStart(swiper) {
            for (let i = 0; i < swiper.slides.length; i++) {
                swiper.slides[i].style.transition = '';
            }
        },
        setTransition(swiper, speed) {
            for (let i = 0; i < swiper.slides.length; i++) {
                swiper.slides[i].style.transition = speed + 'ms';
                swiper.slides[i].querySelector('.facts__item').style.transition = `all ${speed}ms ease 0s`;
            }
        },
        slideChangeTransitionStart(swiper) {
            const activeSlide = [...swiper.slides].find((slide) => slide.classList.contains('swiper-slide-active'));
            const title = activeSlide.querySelector('.facts__item-title');

            animateCSS(title, 'a-fade-up a-delay-200');
        },
    },
});

const swiper = new Swiper(".news-slider", {
    spaceBetween: 20,
    grabCursor: true,
      slidesPerView: "auto",
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
        dynamicBullets: true,
        dynamicMainBullets: 3,
      },
      keyboard: {
        enabled: true,
      },
      navigation: {
            nextEl: ".swiper-button-next",
            prevEl: ".swiper-button-prev",
        },
})


//    var servicesSlider = new Swiper(".services-slider", {
//      effect: "coverflow",
//      grabCursor: true,
//      centeredSlides: true,
//      slidesPerView: "auto",
//      coverflowEffect: {
//        rotate: 50,
//        stretch: 0,
//        depth: 100,
//        modifier: 1,
//        slideShadows: true,
//      },
//      pagination: {
//        el: ".swiper-pagination",
//      },
//    });

let accordion = document.querySelectorAll('.accordion');
let content = document.querySelectorAll('.accordion-content');
accordionFunc()

function accordionFunc() {
    accordion.forEach((el) => {
        let ulList = el.nextElementSibling;
        if (ulList) {
            hideElementLi(ulList)
        }
    })

    document.querySelectorAll('.hide-more').forEach((element) => {
        element.addEventListener('click', (event) => {
            let a = element.parentNode;
            let ulContent = a.parentNode;
            ulContent.style.maxHeight = 180 + 'px';

            setTimeout(funcTime, 280);

            function funcTime() {
                ulContent.classList.remove('ul-li-active');
            }
        })
    })

    document.querySelectorAll('.show-more').forEach((element) => {
        element.addEventListener('click', (event) => {
            let a = element.parentNode;
            let ulContent = a.parentNode;
            ulContent.classList.add('ul-li-active');
            ulContent.style.maxHeight = ulContent.scrollHeight + 'px';
        })
    })

}

accordion.forEach(tab => {
    tab.addEventListener('click', (event) => {
        let targetBrotherEl = event.target.parentNode.nextElementSibling
        event.target.nextElementSibling.nextElementSibling.classList.toggle('open-svg');

        if (targetBrotherEl.classList.contains('accordion-content-active')) {
            if (targetBrotherEl.classList.contains('ul-li-active')) {
                targetBrotherEl.style.maxHeight = null;
                setTimeout(timeOutRemove, 300)

                function timeOutRemove() {
                    targetBrotherEl.classList.remove('accordion-content-active');
                }
            } else {
                targetBrotherEl.style.maxHeight = null

                setTimeout(() => {
                    targetBrotherEl.classList.remove('accordion-content-active')
                }, 300)
            }
        } else {
            targetBrotherEl.classList.toggle('accordion-content-active')
            let targetBrotherElActive = targetBrotherEl.parentNode.querySelector('.accordion-content-active')

            if (targetBrotherElActive) {
                targetBrotherElActive.style.maxHeight = targetBrotherEl.scrollHeight + 'px';
            } else {
                targetBrotherEl.style.maxHeight = null;
            }
        }
    })

})

document.querySelectorAll('.accordion__low').forEach(lowAccordion => {
    lowAccordion.addEventListener('click', (event) => active(event));
});

document.querySelectorAll('.block-click').forEach(blockClick => {
    blockClick.addEventListener('click', (event) => active(event));
});

function active(event) {
    let lowAccordionContent = event.target.nextElementSibling;
    let lowAccordionContentOtIPlus = event.target.parentElement.nextElementSibling;
    let accLow = event.target.closest('.accordion__low')
    let nextAfterAccLow = accLow.nextElementSibling;

    // ваш код для аккордеона и блока с плюсом
    if (event.target.classList.contains('accordion__low')) {
        if (lowAccordionContent.classList.contains('low-accordion-content-active') === false) {
            lowAccordionContent.style.maxHeight = lowAccordionContent.scrollHeight + 'px';
            lowAccordionContent.classList.add('low-accordion-content-active');
            event.target.querySelector('.accordion-svg-plus').classList.add('open-svg-plus');
        } else {
            lowAccordionContent.style.maxHeight = null;
            lowAccordionContent.classList.remove('low-accordion-content-active');
            event.target.querySelector('.accordion-svg-plus').classList.remove('open-svg-plus');
        }
    } else if (event.target.classList.contains('block-click')) {
        if (lowAccordionContentOtIPlus.classList.contains('low-accordion-content-active') === false) {
            lowAccordionContentOtIPlus.style.maxHeight = lowAccordionContentOtIPlus.scrollHeight + 'px';
            lowAccordionContentOtIPlus.classList.add('low-accordion-content-active');
        } else {
            lowAccordionContentOtIPlus.style.maxHeight = null;
            lowAccordionContentOtIPlus.classList.remove('low-accordion-content-active');
        }
    } else if (accLow) {
        if (!nextAfterAccLow.classList.contains('low-accordion-content-active')) {
            nextAfterAccLow.style.maxHeight = nextAfterAccLow.scrollHeight + 'px';
            nextAfterAccLow.classList.add('low-accordion-content-active');

            event.target.closest('.accordion-svg-plus').classList.add('open-svg-plus');
        } else {
            nextAfterAccLow.style.maxHeight = null;
            nextAfterAccLow.classList.remove('low-accordion-content-active');
            event.target.closest('.accordion-svg-plus').classList.remove('open-svg-plus');
        }
    }
}

function hideElementLi(ulList) {
    let liElements = ulList.querySelectorAll('li');
    let lengthLiElements = liElements.length;
    liElements.forEach((liEl, index) => {
        if (index > 4) {
            liEl.classList.add('display-none');
            if (index === 5) {
                liEl.insertAdjacentHTML('beforebegin', '<li><a class="show-more">Показать ещё</a></li>');
            }
            if (index === lengthLiElements - 1) {
                liEl.insertAdjacentHTML('afterend', '<li><a class="hide-more">Cкрыть</a> </li>');
            }
        }
    });
}

const servicesSearchInput = document.querySelector('.services-page input[name="search"]')
const servicesTabs = document.querySelectorAll(".services-page .headings__item.tab")
const servicesItemsContainer = document.querySelector(".services__items")
const servicesItemsNotFound = document.querySelector(".services__items-not-found")


function reinitServicesModals() {
    document.querySelectorAll(".services-page [data-modal]").forEach(modalButton => {
        const modalId = modalButton.dataset.modal;
        const modal = document.querySelector(`.modal[id="${modalId}"]`)
        if (modal) {
            modalButton.addEventListener("click", () => {
                onOpenModal(modal)
                let serviceName = modalButton.dataset.serviceName;
                let modalServiceTitle = modal.querySelector(".modal__service-name");
                let modalServiceInput = modal.querySelector('input[name="service"]')
                if (serviceName) {
                    if (modalServiceTitle) modalServiceTitle.innerText = serviceName
                    if (modalServiceInput) modalServiceInput.value = serviceName
                }
            })
        }
    })
}

servicesSearchInput?.addEventListener("input", () => {
    servicesItemsNotFound.classList.remove("active")
    servicesItemsContainer.classList.remove("d-none")
    let value = servicesSearchInput.value.trim().toLowerCase()
    if (!value) {
        document.querySelectorAll(".services__item").forEach(el => {
            el.classList.remove("hidden")
        })
    } else {
        document.querySelectorAll(".services__item").forEach(el => {
            if (el.querySelector(".services__item-description_title").innerText.toLowerCase().includes(value)) {
                el.classList.remove("hidden")
            } else {
                el.classList.add("hidden")
            }
        })
    }

    if (!document.querySelector(".services__item:not(.hidden)")) {
        servicesItemsContainer.classList.add("d-none")
        servicesItemsNotFound.classList.add("active")
    }
})

servicesTabs.forEach(tab => {
    tab.addEventListener("click", (e) => {
        e.preventDefault()
        servicesItemsContainer.classList.remove("d-none")
        servicesItemsNotFound.classList.remove("active")
        servicesTabs.forEach(el => el.classList.remove("active"))
        tab.classList.add("active")
        fetch(tab.dataset.path)
            .then(response => response.text())
            .then(text => {
                let parser = new DOMParser().parseFromString(text, "text/html")
                document.querySelector("h1").innerHTML = parser.querySelector("h1").innerHTML;
                document.querySelector("title").innerHTML = parser.querySelector("title").innerHTML;
                document.querySelector(".services__items").innerHTML = parser.querySelector(".services__items").innerHTML;
                document.querySelector(".breadcrumbs").innerHTML = parser.querySelector(".breadcrumbs").innerHTML;
                reinitServicesModals()
                window.history.pushState("", "", tab.dataset.path)
            })
    })
})

if (servicesItemsContainer && servicesItemsNotFound && !document.querySelector(".services__item:not(.hidden)")) {
    servicesItemsContainer.classList.add("d-none")
    servicesItemsNotFound.classList.add("active")
}


const articlesSearchInput = document.querySelector('.blog input[name="search"]')
const articlesTabs = document.querySelectorAll(".blog .headings__item.tab")
const articlesItemsContainer = document.querySelector(".articles__items")
const articlesItemsNotFound = document.querySelector(".articles__items-not-found")

articlesSearchInput?.addEventListener("input", () => {
    articlesItemsNotFound.classList.remove("active")
    articlesItemsContainer.classList.remove("d-none")
    let value = articlesSearchInput.value.trim().toLowerCase()
    if (!value) {
        document.querySelectorAll(".articles__item").forEach(el => {
            el.classList.remove("hidden")
        })
    } else {
        document.querySelectorAll(".articles__item").forEach(el => {
            if (el.querySelector(".articles__item-description_title").innerText.toLowerCase().includes(value)) {
                el.classList.remove("hidden")
            } else {
                el.classList.add("hidden")
            }
        })
    }

    if (!document.querySelector(".articles__item:not(.hidden)")) {
        articlesItemsContainer.classList.add("d-none")
        articlesItemsNotFound.classList.add("active")
    }
})

articlesTabs.forEach(tab => {
    tab.addEventListener("click", (e) => {
        e.preventDefault()
        articlesItemsContainer.classList.remove("d-none")
        articlesItemsNotFound.classList.remove("active")
        articlesTabs.forEach(el => el.classList.remove("active"))
        tab.classList.add("active")
        fetch(tab.dataset.path)
            .then(response => response.text())
            .then(text => {
                let parser = new DOMParser().parseFromString(text, "text/html")
                document.querySelector("h1").innerHTML = parser.querySelector("h1").innerHTML;
                document.querySelector("title").innerHTML = parser.querySelector("title").innerHTML;
                document.querySelector(".articles__items").innerHTML = parser.querySelector(".articles__items").innerHTML;
                document.querySelector(".breadcrumbs").innerHTML = parser.querySelector(".breadcrumbs").innerHTML;
                window.history.pushState("", "", tab.dataset.path)
            })
    })
})

if (articlesItemsContainer && articlesItemsNotFound && !document.querySelector(".articles__item:not(.hidden)")) {
    articlesItemsContainer.classList.add("d-none")
    articlesItemsNotFound.classList.add("active")
}

const subscribeFocusLink = document.querySelector("#subscribe-focus-link");
const subscriptionForm = document.querySelector(".subscription__form");

if (subscribeFocusLink && subscriptionForm) {
    subscribeFocusLink.addEventListener("click", () => {
        subscriptionForm.querySelector('input[type="email"]').focus()
    })
}

const priceListSearchInput = document.querySelector('.price-list input[name="search"]')
const priceListItemsContainer = document.querySelector(".price-list__wrapper")
const priceListItemsNotFound = document.querySelector(".price-list__not-found")

priceListSearchInput?.addEventListener("input", () => {
    priceListItemsNotFound.classList.remove("active")
    priceListItemsContainer.classList.remove("d-none")
    let value = priceListSearchInput.value.trim().toLowerCase()
    if (!value) {
        document.querySelectorAll(".table-section").forEach(el => {
            el.classList.remove("hidden")
        })
    } else {
        document.querySelectorAll(".table-section").forEach(el => {
            if (el.querySelector(".table-group__title").innerText.toLowerCase().includes(value)) {
                el.classList.remove("hidden")
            } else {
                el.classList.add("hidden")
            }
        })
    }

    if (!document.querySelector(".table-section:not(.hidden)")) {
        priceListItemsContainer.classList.add("d-none")
        priceListItemsNotFound.classList.add("active")
    }
})

const priceListTableGroups = document.querySelectorAll(".table-group")
priceListTableGroups.forEach(group => {
    const groupTitle = group.querySelector(".table-group__title")
    groupTitle?.addEventListener("click", () => {
        if (group.classList.contains("opened")) {
            group.classList.remove("opened")
        } else {
            group.classList.add("opened")
        }
    })
})


const readMoreButtons = document.querySelectorAll("[data-read-more]")
readMoreButtons.forEach(btn => {
    btn.addEventListener("click", () => {
        const textBlock = document.querySelector('[data-read-more-target]')
        if (textBlock) {
            window.scrollTo({
                top: textBlock.getBoundingClientRect().top + window.pageYOffset - document.querySelector("header").offsetHeight - 20,
                behavior: 'smooth'
            });
        }
    })
})


document.querySelectorAll(".contract__tabs-head").forEach(tab => {
    tab.addEventListener("click", () => {
        document.querySelectorAll(".contract__tabs-head").forEach(el => {
            el.classList.remove("active")
        })
        tab.classList.add("active")
        document.querySelectorAll(".contract__tabs-content").forEach(content => {
            if (content.dataset.tab === tab.dataset.tab) {
                content.classList.add("active")
            } else {
                content.classList.remove("active")
            }
        })
    })
})


const whatsappLinks = document.querySelectorAll(".whatsapp-link")
whatsappLinks.forEach(link => link.addEventListener("click", whatsappLinkOnclick))
function whatsappLinkOnclick(e) {
    let md = new MobileDetect(window.navigator.userAgent);
    let number = e.currentTarget.dataset.number
    if (!number) return
    e.preventDefault()
    if (md.mobile()) {
        window.open("whatsapp://send?phone=" + number, '_blank')
    } else {
        window.open("https://web.whatsapp.com/send/?phone=" + number, '_blank')
    }
}

document.querySelectorAll(".team-faq__item-title").forEach(el => {
    el.addEventListener("click", (e) => {
        let faqItem = el.parentElement
        if (faqItem.classList.contains("opened")) {
            faqItem.classList.remove("opened")
        } else{
            faqItem.classList.add("opened")
        }
    })
})
