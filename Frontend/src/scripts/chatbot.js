(function () {
  ChatbotContainer = document.getElementById("ChatbotContainerMain");
  MiniChatbot = document.getElementById("MiniChatbot");
  MiniChatbotValuechange = document.querySelector("#MiniChatbotValue use");
  btn = document.getElementById("Chatbot");
  spaner = document.getElementById("closeChatbot");
  ChatbotSuggestedQuestions = document.getElementById(
    "ChatbotSuggestedQuestions"
  );
  querysearch = document.getElementById("querysearch");
  chatSpace = document.getElementById("Chat-space");

  userid = localStorage.getItem("Rsession_name");
  reseter = document.getElementById("reset");
})();

btn.onclick = function () {
  ChatbotContainer.style.display = "flex";
  ChatbotContainer.style.display = "flex";
  querysearch.focus();
};
spaner.onclick = function () {
  ChatbotContainer.style.display = "none";
};

console.log(userid);
send_data = {
  query: "",
  // "query": query,
  resume_filters: {
    Candidate: {
      check: [],
    },
    Education: {
      check: [],
    },
    WorkExperience: {
      check: [],
    },
    Contact: {
      check: [],
    },
    Skill: {
      check: [],
    },
    Address: {
      check: [],
    },
    ResumeIdList: {
      check: [],
      ResumeIdValue: [],
    },
  },
  count: 0,
  user: "userid1",
};

MiniChatbot.onclick = function () {
  if (
    MiniChatbotValuechange.getAttribute("xlink:href") ===
    "./Icons/icons.svg#Maximize"
  ) {
    ChatbotContainer.classList.add("mini");
    MiniChatbotValuechange.setAttribute(
      "xlink:href",
      "./Icons/icons.svg#minimize"
    );
  } else {
    ChatbotContainer.classList.remove("mini");
    MiniChatbotValuechange.setAttribute(
      "xlink:href",
      "./Icons/icons.svg#Maximize"
    );
  }
};

querysearch.addEventListener("keydown", (event) => {
  if (
    event.key === "Enter" &&
    event.target.value.length > 0 &&
    !FilteringData.QueryonProcess
  ) {
    FilteringData.QueryonProcess = true;
    ChatbotSuggestedQuestions.style.display = "none";
    value = event.target.value.replace(/\s+/g, " ").trim();
    chat(value);
    querysearch.value = "";
  }
});

function submitQuery(event) {
  const queryInput = document.getElementById("queryInput");
  if (!queryInput.value.trim()) {
    event.preventDefault(); // Prevent form submission
    alert("Please enter a query!"); // Show an alert or handle the empty input
  } else {
    var recentQuesDiv = document.getElementById("recent-ques");
    recentQuesDiv.classList.add("hidden");
    chat(event);
  }
}

async function chat(value) {
  FilteringData.onFolderSelect = "";
  if (FilteringData.page === "data") {
    ClearHistory();
    toCheckSearchHistory();
  }

  chatSpace.style.minHeight = "40vh";
  const query = value;
  const UserQuery = document.createElement("p");
  UserQuery.classList.add("right");
  UserQuery.textContent = query;
  chatSpace.appendChild(UserQuery);
  chatSpace.scrollTop = chatSpace.scrollHeight;

  send_data["query"] = query;
  console.log("archit1", send_data);
  ////////////////////////////////////////
  try {
    const response = await fetch("http://localhost:8000/chatbot", {
      // const response = await fetch("http://localhost:8000/chatbot", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(send_data),
    });
    const data = await response.json();
    console.log("archit");
    console.log("data fetched", data);
    if (data[0] === "exit") {
      FilteringData.QueryonProcess = false;
      ChatbotContainer.style.display = "none";
      ChatbotSuggestedQuestions.style.display = "flex";
      chatSpace.innerHTML = "";
      chatSpace.style.minHeight = "0";
    } else if (typeof data[0] === "string") {
      console.log("check string");
      const messageElement = document.createElement("p");
      messageElement.classList.add("left");
      messageElement.textContent = data[0];
      chatSpace.appendChild(messageElement);
      chatSpace.scrollTop = chatSpace.scrollHeight;
      FilteringData.QueryonProcess = false;
    } else if (
      typeof data[0] === "object" &&
      data !== null &&
      !Array.isArray(data[0])
    ) {
      datastring = Object.values(data[0])[0];
      const messageElement = document.createElement("p");
      messageElement.classList.add("left");
      messageElement.textContent = "Your Results Displayed";
      chatSpace.appendChild(messageElement);

      FilteringData.onSelectSubFolder = datastring;
      FilteringData.chatbotData = false;
      FilteringData.onFolderValue = true;
      FilteringData.QueryonProcess = false;
      FilteringData.page = "data";
      chatSpace.scrollTop = chatSpace.scrollHeight;
      ChatbotContainer.style.display = "none";
      await triggerDOMContentLoaded();
    } else {
      // resumes = data[0].slice(0, 10);
      send_data["resume_filters"] = data[1];
      send_data["count"] = data[2];
      console.log(data[3]);
      // document.getElementById("paraelemnet").textContent = data[3];
      // let send_data_str = JSON.stringify(send_data);
      let resumeids = JSON.stringify(data[0]);

      FilteringData.chatbotResumeIds = resumeids;
      FilteringData.chatbotData = true;
      // sessionStorage.setItem("send_data", send_data_json);
      console.log("after the mess");
      console.log(send_data);
      // let url = "resumeDisplay.html";
      // // Redirect to the new URL
      // // window.location.href = url;
      // window.location.replace(url);
      const messageElement = document.createElement("p");
      messageElement.classList.add("left");
      messageElement.textContent = "Results for " + data[3];
      chatSpace.appendChild(messageElement);
      chatSpace.scrollTop = chatSpace.scrollHeight;
      FilteringData.page = "data";
      FilteringData.QueryonProcess = false;
      ChatbotContainer.style.display = "none";
      await triggerDOMContentLoaded();
      FilteringData.dataparaelement = data[3];
    }
    return data;
  } catch (error) {
    console.error("Error:", error);
  }
  ///////////////////////////////////////
  // fetch("http://localhost:8000/chatbot", {
  //     method: "POST",
  //     headers: {
  //         "Content-Type": "application/json",
  //     },
  //     body: JSON.stringify(send_data),
  // })
  //     .then((response) => response.json())
  //     // .then((data) => {
  //     //     console.log(data);
  //     // })
  //     .then((data) => {
  //         console.log("archit")
  //         console.log(data)
  //         var queryInput = document.getElementById('queryInput');
  //         queryInput.value = '';
  //         // console.log(resumes.slice(0, 5))
  //         // console.log(data[1].slice(0, 10));
  //         // resumes.map((record) => {
  //         //     const messageElement = document.createElement('p');
  //         //     messageElement.classList.add('left');
  //         //     messageElement.textContent = `${record[1]}  (${record[4].slice[0, 8]}) - ${record[5].slice[0, 8]}`;
  //         //     chatSpace.appendChild(messageElement);
  //         // });
  //         console.log(data[0], typeof data[0])
  //         if (data[0] === "exit") {
  //             var modal = document.getElementById("myModal");
  //             modal.style.display = "none";
  //         }
  //         else if (typeof data[0] === 'string') {
  //             console.log("check string");
  //             const messageElement = document.createElement('p');
  //             messageElement.classList.add('left');
  //             messageElement.textContent = data[0]
  //             chatSpace.appendChild(messageElement);
  //         } else {
  //             //
  //             resumes = data[0].slice(0, 10);
  //             send_data["resume_filters"] = data[1]
  //             send_data["count"] = data[2]
  //             // updateJson(data[1], data[2])
  //             let send_data_str = JSON.stringify(send_data);
  //             localStorage.setItem('send_data', send_data_str);
  //             sessionStorage.setItem('send_data', send_data_json);
  //             console.log("after the mess")
  //             console.log(send_data)
  //             let url = 'resumeDisplay.html'
  //             // Redirect to the new URL
  //             // window.location.href = url;
  //             // window.location.replace(url);
  //         }
  //         return data;
  //     })
  //     .catch((error) => {
  //         console.error("Error:", error);
  //     });
}
// data = {
//     "query": "get me data on java",
//     // "query": query,
//     "resume_filters": {
//         "Candidate": {
//             "check": [],
//         },
//         "Education": {
//             "check": [],
//         },
//         "WorkExperience": {
//             "check": [],
//         },
//         "Contact": {
//             "check": [],
//         },
//         "Skill": {
//             "check": [],
//         },
//     },
//     "count": 0
// }
// fetch("http://localhost:8000/chatbot", {
//     method: "POST",
//     headers: {
//         "Content-Type": "application/json",
//     },
//     body: JSON.stringify(data),
// })
//     .then((response) => response.json())
//     // .then((data) => {
//     //     console.log(data);
//     // })
//     .then((data) => {
//         console.log(data)
//     })
//     .catch((error) => {
//         console.error("Error:", error);
//     });
function addQuestion(button) {
  console.log();
  var paragraph = button.querySelector("p");

  var question = paragraph.textContent.replace(/\s+/g, " ").trim();

  console.log(question);
  ChatbotSuggestedQuestions.style.display = "none";
  FilteringData.QueryonProcess = true;
  chat(question);
}
function resetQuery() {
  var queryInput = document.getElementById("querysearch");
  queryInput.value = "";
}
// window.send_data = send_data
// chat()

// reset

reseter.addEventListener("click", () => {
  ChatbotSuggestedQuestions.style.display = "flex";
  FilteringData.QueryonProcess = false;
  chatSpace.innerHTML = "";
  chatSpace.style.minHeight = "0";
  resetQuery();
});
