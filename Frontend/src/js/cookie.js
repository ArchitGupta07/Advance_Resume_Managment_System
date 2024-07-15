setCookie = (name, token, time) => {
  var validation_date = "";
  if (time) {
    var date = new Date();
    date.setDate(date.getDate() + time);
    validation_date = "; expires=" + date.toUTCString();
  }
  document.cookie = name + "=" + (token || "") + validation_date + "; path=/";
};

getCookie = (name) => {
  let nameEQ = name + "=";
  var cookies = document.cookie.split(";");
  for (var i = 0; i < cookies.length; i++) {
    var cookie = cookies[i];
    while (cookie.charAt(0) == " ") {
      cookie = cookie.substring(1, cookie.length);
      console.log(cookie);
    }
    if (cookie.indexOf(nameEQ) == 0) {
      return cookie.substring(nameEQ.length, cookie.length);
    }
  }
  return null;
};

isLogin = () => {
  let cookieData = localStorage.getItem("Rsession_name");
  if (getCookie(cookieData) !== null) {
    window.location.replace("main.html");
  }
};

isLogout = () => {
  let cookieData = localStorage.getItem("Rsession_name");
  if (getCookie(cookieData) === null) {
    window.location.replace("index.html");
  }
};

function redirectToCustomPath(customPath) {
  var newPath = window.location.origin + "/" + customPath;
  window.history.pushState({}, "", newPath);
  window.location.replace(newPath);
}

window.setCookie = setCookie;
window.getCookie = getCookie;
window.isLogin = isLogin;
window.isLogout = isLogout;
