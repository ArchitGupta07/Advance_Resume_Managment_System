getHtml = async () => {
  try {
    const response = await fetch("Header.html");
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    const data = await response.text();
    const parser = new DOMParser();
    const htmlDocument = parser.parseFromString(data, "text/html");

    // const temContainer = document.createElement("div");
    // temContainer.innerHTML = data;
    const scripts = htmlDocument.querySelectorAll("script");
    for (i of scripts) {
      var script = document.createElement("script");
      script.src = i.src;
      document.body.appendChild(script);

      // console.log(scripts)
    }
    document.getElementById("Header").innerHTML = "";
    const specificContainer = htmlDocument.querySelector("#HeaderContainer");
    specificContainer.childNodes.forEach((node) => {
      document.getElementById("Header").appendChild(node.cloneNode(true));
    });

    console.log("Complete");
  } catch (error) {
    console.error("Error fetching header:", error);
  }
};

// document.addEventListener("DOMContentLoaded", function () {
//   getHtml();
// });

// document.addEventListener("DOMContentLoaded", async function () {
//   await getHtml();
// });

// window.onload = async () => {
//   await getHtml();
// };

ScriptChecker = (value) => {
  const scriptSrcToCheck = value;

  const scriptElements = document.body.getElementsByTagName("script");

  const scriptArray = Array.from(scriptElements);

  const scriptExists = scriptArray.some(
    (script) => script.src === scriptSrcToCheck
  );
  return scriptExists;
};

getMainHtml = async (value) => {
  try {
    const response = await fetch("welcome.html");
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }

    const existingScripts = document.body.querySelectorAll("script");
    existingScripts.forEach((script) => {
      if (script.src.split("/").slice(-1)[0] === "data.js") {
        script.parentNode.removeChild(script);
      }
    });

    const data = await response.text();
    const parser = new DOMParser();
    const htmlDocument = parser.parseFromString(data, "text/html");
    // document.head.innerHTML = "";

    // const headContent = htmlDocument.querySelector("head").innerHTML;
    // document.head.innerHTML = headContent;

    var script = document.createElement("script");
    script.src = "./js/Dashboard.js";
    console.log(ScriptChecker("./js/Dashboard.js"));
    if (!ScriptChecker("./js/Dashboard.js")) {
      document.body.appendChild(script);
    }

    const specificContainer = htmlDocument.querySelector("#WelcomeMain");
    document.getElementById("mainContent").innerHTML = "";

    specificContainer.childNodes.forEach((node) => {
      document.getElementById("mainContent").appendChild(node.cloneNode(true));
    });

    console.log("Complete");
  } catch (error) {
    console.error("Error fetching header:", error);
  }
};

// document.addEventListener("DOMContentLoaded", function () {
//   getHtml();
// });

// document.addEventListener("DOMContentLoaded", async function () {
//   await getHtml();
// });

// window.onload = async () => {
//   await getHtml();
// };

getContentHtml = async () => {
  try {
    const response = await fetch("data.html");
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }

    const existingScripts = document.body.querySelectorAll("script");
    existingScripts.forEach((script) => {
      if (script.src.split("/").slice(-1)[0] === "Dashboard.js") {
        script.parentNode.removeChild(script);
      }
    });

    const data = await response.text();
    const parser = new DOMParser();
    const htmlDocument = parser.parseFromString(data, "text/html");
    console.log(htmlDocument);
    // document.head.innerHTML = "";

    // const headContent = htmlDocument.querySelector("head").innerHTML;
    // document.head.innerHTML = headContent;
    // const temContainer = document.createElement("div");
    // temContainer.innerHTML = data;

    var script = document.createElement("script");
    script.src = "./js/data.js";

    // document.body.appendChild(script);

    // console.log(scripts)
    if (!ScriptChecker("./js/data.js")) {
      document.body.appendChild(script);
    }

    document.getElementById("mainContent").innerHTML = "";

    const specificContainer = htmlDocument.querySelector("#dataMain");
    specificContainer.childNodes.forEach((node) => {
      document.getElementById("mainContent").appendChild(node.cloneNode(true));
    });

    console.log("Complete");
  } catch (error) {
    console.error("Error fetching header:", error);
  }
};

window.getMainHtml = getMainHtml;
window.getContentHtml = getContentHtml;
window.getHtml = getHtml;
