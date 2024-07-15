document.addEventListener("DOMContentLoaded", function () {
  const slides = document.querySelectorAll(".LoginPage-CarouselImages");
  const dots = document.querySelectorAll(".dot");
  let currentIndex = 0;

  function showSlide(index) {
    const offset = -index * 100;
    slides.forEach((slide, i) => {
      slide.style.transform = `translateX(${offset}%)`;
      dots[i].classList.toggle("active", i === index);
    });
    currentIndex = index;
  }

  dots.forEach((dot, i) => {
    dot.addEventListener("click", () => showSlide(i));
  });

  function nextSlide() {
    currentIndex = (currentIndex + 1) % slides.length;
    showSlide(currentIndex);
  }

  setInterval(nextSlide, 3000);
});

// Password
let icon = document.getElementById("Icon");
let iconValue = document.querySelector("#IconValue use");

icon.onclick = function () {
  if (
    iconValue.getAttribute("xlink:href") === "./Icons/icons.svg#PasswordIcon"
  ) {
    document.getElementById("Loginpassword").setAttribute("type", "text");
    iconValue.setAttribute("xlink:href", "./Icons/icons.svg#PasswordUnHide");
  } else {
    document.getElementById("Loginpassword").setAttribute("type", "password");
    iconValue.setAttribute("xlink:href", "./Icons/icons.svg#PasswordIcon");
  }
};

//
function toFocus() {
  document.getElementById("responsePara").textContent = "";
}
