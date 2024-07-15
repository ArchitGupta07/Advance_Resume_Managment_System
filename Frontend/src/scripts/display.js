// let myVariable = window.myVariable;
// let send_data_str = localStorage.getItem("send_data");
// let send_data = JSON.parse(send_data_str);
let all_resumes = localStorage.getItem("resumeids");
// let resumeids = JSON.parse(all_resumes);
// sendDATA["count"] = 10
// window.myVariable = sendDATA
// console.log("Before change:", send_data);

async function onDomLoaded() {
  TotalValue = document.getElementById("TotalValue");
  // Your JavaScript code goes here
  console.log("DOM has fully loaded");
  fetchData();
  // Add any other code you want to execute
}
// Add an event listener for the DOMContentLoaded event
document.addEventListener("DOMContentLoaded", onDomLoaded);
// let listItems = document.getElementById("listItems");
// var filterJson = require('filterLog.json')
// console.log(filterJson)
function fetchData() {
  // console.log(send_data["resume_filters"]);
  console.log("localstorage data", resumeids);
  console.log(JSON.stringify(resumeids));
  // fetch("http://localhost:8000/displayfilter", {
  fetch("http://localhost:8000/full_resume_data", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(resumeids),
  })
    .then((response) => response.json())
    // .then((data) => {
    //     console.log(data);
    // })
    .then((data) => {
      console.log("got data", data);
      toShowData(data);
      // resumes = data[0].slice(0, 10);
      // // console.log(resumes.slice(0, 5))
      // // console.log(data[1].slice(0, 10));
      // resumes.map((record) => {
      //     const messageElement = document.createElement('p');
      //     messageElement.classList.add('left');
      //     messageElement.textContent = `${record[1]}  (${record[4].slice[0, 8]}) - ${record[5].slice[0, 8]}`;
      //     chatSpace.appendChild(messageElement);
      // });
      // send_data["resume_filters"] = data[1]
      // console.log(query)
      // console.log(send_data)
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}
// function toShowData(data) {
//   if (data.length !== 0) {
//     // data = data[0];
//     // lst = [];
//     // items = {};
//     for (let i of data) {
//       // console.log(i);
//       let li = document.createElement("li");
//       let ResumeId = document.createElement("p");
//       ResumeId.textContent = i[0];
//       let FirstName = document.createElement("p");
//       FirstName.textContent = i[1];
//       // let contactvalue = Array.from(items[i].Contact);
//       let Contact_type = document.createElement("p");
//       Contact_type.textContent = i[2];
//       let Contact_value = document.createElement("p");
//       Contact_value.textContent = i[3];
//       let SkillName = document.createElement("button");
//       SkillName.classList.add("SkillElement");
//       SkillName.textContent = "Skills";
//       SkillName.addEventListener("mouseover", () => {
//         // content = Array.from(items[i].SkillName);
//         toUpadteSkillContainer(i[4]);
//         SkillsContainer.style.display = "block";
//       });
//       SkillName.addEventListener("mouseout", () => {
//         SkillsContainer.textContent = "";
//         SkillsContainer.style.display = "none";
//       });
//       let Experience = document.createElement("button");
//       Experience.classList.add("SkillElement");
//       Experience.textContent = "Experience";
//       Experience.addEventListener("mouseover", () => {
//         // content = Array.from(items[i].SkillName);
//         toUpadteSkillContainer(i[5]);
//         SkillsContainer.style.display = "block";
//       });
//       Experience.addEventListener("mouseout", () => {
//         SkillsContainer.textContent = "";
//         SkillsContainer.style.display = "none";
//       });
//       li.appendChild(ResumeId);
//       li.appendChild(FirstName);
//       li.appendChild(Contact_value);
//       li.appendChild(SkillName);
//       li.appendChild(Experience);
//       li.classList.add("elementStyle");
//       listItems.appendChild(li);
//     }
//     // if (method === "GET") {
//     //     Filterdata.ResumeIdList.ResumeIdValue = lst2;
//     //     // console.log(Filterdata);
//     // }
//   } else {
//     let li = document.createElement("li");
//     li.textContent = "No data";
//     listItems.appendChild(li);
//   }
// }
