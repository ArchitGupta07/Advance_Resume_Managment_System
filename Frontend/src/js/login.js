async function digestMessage(message) {
  const msgUint8 = new TextEncoder().encode(message);
  const hashBuffer = await crypto.subtle.digest("SHA-256", msgUint8);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  const hashHex = hashArray
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
  return hashHex;
}

togetLoginDetails = async (newJsonData, data = null) => {
  if (data !== null) {
    let hasedvalue = await digestMessage(data);
    newJsonData["Password"] = hasedvalue;
  }

  let url = new URL("http://localhost:8000/login/");
  url.search = new URLSearchParams(newJsonData).toString();
  await fetch(url, {
    method: "GET",
  })
    .then((response) => {
      if (!response.ok) {
        document.getElementById("LoginForm").reset();
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => toLoginValidate(data))
    .catch((error) => alert(error));
};

toLoginValidate = (data) => {
  if (data.statusCode) {
    document.getElementById("LoginForm").reset();
    console.log(data);
    localStorage.setItem("Rsession_name", data.session_name);
    localStorage.setItem("value", true);
    setCookie(data.session_name, data.session_token, data.validation_time);

    window.location.replace("main.html");

    // document.getElementById("responsePara").textContent = "";
  } else {
    ErrorHandler(data.error);
    // document.getElementById("responsePara").textContent = data.error;
    // document.getElementById("LoginForm").reset();
  }
};

loginCertindiatls = () => {
  if (
    document.getElementById("Loginusername").value === "" &&
    document.getElementById("Loginpassword").value === ""
  ) {
    // document.getElementById("Input1").style.borderColor = "red";
    // document.getElementById("Input2").style.borderColor = "red";

    document.getElementById("responsePara").textContent =
      "Please Enter Your Credentials";
  } else if (document.getElementById("Loginusername").value === "") {
    // document.getElementById("Input1").style.borderColor = "red";
    document.getElementById("responsePara").textContent =
      "Please Enter Your Username";
  } else if (document.getElementById("Loginpassword").value === "") {
    // document.getElementById("Input2").style.borderColor = "red";

    document.getElementById("responsePara").textContent =
      "Please Enter Your Password";
  } else {
    return true;
  }
};

toFocus = () => {
  document.getElementById("responsePara").textContent = "";
  document.getElementById("Input1").style.borderColor = "";
  document.getElementById("Input2").style.borderColor = "";
};

document
  .getElementById("LoginForm")
  .addEventListener("submit", function (event) {
    event.preventDefault();
    if (loginCertindiatls()) {
      const formData = new FormData(this);
      const formDataJson = Object.fromEntries(formData.entries());
      const newJsonData = {
        Email: formDataJson.Email.toLocaleLowerCase(),
      };

      // Using api Function
      togetLoginDetails(newJsonData, formDataJson["Password"]);
    }
  });

ErrorHandler = (message) => {
  document.getElementById("responsePara").textContent = message;
  // this.setTimeout(() => {
  //   ErrorContainer.classList.remove("Error-Container");
  //   ErrorContainer.textContent = "";
  // }, 2000);
  // ErrorContainer.classList.add("Error-Container");
  // ErrorContainer.textContent = message;
};

window.onload = () => {
  isLogin();
};
