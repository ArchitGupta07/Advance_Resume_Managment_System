(function () {
  CategoryCreate = document.getElementById("CategoryCreate");
  loader = document.getElementById("loader");
  datalistItems = document.getElementById("datalistItems");
  viewcandidatedata = document.getElementById("viewcandidatedata");
  paraelemnet = document.getElementById("paraelemnet");
  DashboardFolderName = document.getElementById("DashboardFolderName");
  BackArrow = document.getElementById("BackArrow");
  sortedorder = "asc";
  sortedordervalue = 0;
  itemsPerPage = 10;
  currentPage = 1;
  paginationData = "";
  VisibleTimout = "";
})();

// removeFunction = (id) => {
//   const para1 = document.getElementById(id);
//   console.log(para1);
//   para1.parentNode.removeChild(para1);
//   Filterdata.Skill.SkillName = Filterdata.Skill.SkillName.filter(
//     (item) => item.uniqueId !== id
//   );
// };
tocheck = (data) => {
  data = JSON.parse(JSON.stringify(data));
  for (let i of Object.keys(data)) {
    for (let j of Object.keys(data[i])) {
      if (data[i][j].length > 0 && j !== "check") {
        data[i]["check"].push(j);
        data[i][j] = data[i][j].map((item) => item[j]);
      } else {
        if (j !== "check") {
          delete data[i][j];
        }
      }
    }
  }
  console.log(data);
  return data;
};

toget = async (
  url = "http://localhost:8000/displayfilter/",
  method = "POST",
  data = Filterdata,
  value = true
) => {
  console.log(value);
  if (value === true) {
    data = method === "POST" ? tocheck(data) : "";
  } else {
    data = data;
  }
  console.log(url, method, data);
  options =
    method === "GET"
      ? { method: method }
      : {
        method: method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      };
  console.log(options);
  await fetch(url, options)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      console.log("this is data js file: ", data);
      FilteringData.FetchedData =
        data[1] !== null
          ? Object.keys(data[1]).map((item) => data[1][item])
          : [];
      FilteringData.TemporaryData = FilteringData.FetchedData;
      displayItems(data, 1);
    });
};

function generateUniqueId() {
  const randomNumber = Math.random().toString(16).slice(2);
  const timestamp = Date.now().toString(16);
  const uniqueId = timestamp + randomNumber;
  return uniqueId;
}

// Skills.addEventListener("change", function (e) {
//   console.log(e.target.value);
// });

// Locations.addEventListener("change", function (event) {
//   Filterdata.WorkExperience.Location = [];
//   data = {
//     uniqueId: generateUniqueId(),
//     Location: event.target.value,
//   };

//   if (event.target.value === "All") {
//     Filterdata.WorkExperience.Location = [];
//   } else {
//     Filterdata.WorkExperience.Location.push(data);
//   }
// });

// Skills.addEventListener("keydown", function (event) {
//   if (event.key === "Enter") {
//     let value = event.target.value;
//     value = value.split(",");
//     for (let i of value) {
//       const data = {
//         uniqueId: generateUniqueId(),
//         SkillName: i,
//       };
//       let para = document.createElement("p");
//       para.textContent = i + " X ";
//       para.id = data.uniqueId;
//       para.onclick = function () {
//         removeFunction(data.uniqueId);
//       };
//       skillstext.appendChild(para);
//       Filterdata.Skill.SkillName.push(data);
//     }
//     Skills.value = "";
//   }
// });

// Degree.addEventListener("change", function (event) {
//   Filterdata.Education.Degree = [];

//   data = {
//     uniqueId: generateUniqueId(),
//     Degree: event.target.value,
//   };
//   // DegreeText.textContent = DegreeText.textContent + event.target.value + " X ";
//   if (event.target.value === "All") {
//     Filterdata.Education.Degree = [];
//   } else {
//     Filterdata.Education.Degree.push(data);
//   }
// });

// InputDetais.addEventListener("keydown", function (event) {
//   if (event.key === "Enter" && InputDetais.value !== "") {
//     if (CandidateDetails.value !== "None") {
//       const data = {
//         uniqueId: generateUniqueId(),
//         details: event.target.value,
//       };
//       Filterdata.Candidate[CandidateDetails.value].push(data);
//       console.log(Filterdata);
//       InputDetais.value = "";
//     } else {
//       alert("Please select a candidate above Option");
//     }
//   }
// });

// Experience.addEventListener("change", function (event) {
//   Filterdata.Candidate.experience = [];

//   data = {
//     uniqueId: generateUniqueId(),
//     experience: event.target.value,
//   };
//   if (event.target.value === "All") {
//     Filterdata.Candidate.experience = [];
//   } else {
//     Filterdata.Candidate.experience.push(data);
//   }
// });

// Submit.addEventListener("click", function () {
//   toget(Filterdata);
//   console.log(Filterdata);
//   listItems.innerHTML = "";
// });

// // Prams from pages
// function getQueryParam(param) {
//   const queryString = window.location.search;
//   const urlParams = new URLSearchParams(queryString);
//   return urlParams.get(param);
// }

function toLoadContent() {
  try {
    loader.style.display = "flex";
    const dataString = FilteringData.onSelectSubFolder;
    const searchvalue = FilteringData.onFolderValue;
    const chatbotData = FilteringData.chatbotData;
    console.log(dataString, searchvalue, chatbotData);
    if (dataString && !chatbotData) {
      const data = dataString;
      document.getElementById("heading").textContent = data;
      DashboardFolderName.textContent =
        FilteringData.onFolderSelect != ""
          ? " - " + FilteringData.onFolderSelect
          : "";
      console.log(searchvalue);
      if (searchvalue === false) {
        let data1 = {
          query: data,
        };
        console.log(data1);
        let url = new URL("http://localhost:8000/search_query/");
        const method = "POST";
        toget(url, method, data1, false);
      } else {
        let data1 = {
          category_data: data,
        };
        console.log(data1);
        let url = new URL("http://localhost:8000/displayskillmap/");
        url.search = new URLSearchParams(data1).toString();
        method = "GET";
        toget(url, method);
      }
    } else {
      document.getElementById("heading").textContent = "Chatbot Results";
      FilteringData.onFolderValue = false;
      let url = new URL("http://localhost:8000/full_resume_data");
      let method = "POST";
      console.log(FilteringData.chatbotResumeIds);
      toget(url, method, JSON.parse(FilteringData.chatbotResumeIds), false);
    }
  } catch (e) {
    alert(e.toString());
    loader.style.display = "none";
  }
}
toLoadContent();
// Show Skill Container
toUpdateSkillContainer = function (data, id, item) {
  let Listid = document.getElementById(id);
  let Listitem = document.getElementById(item);
  let boundaries = Listid.getBoundingClientRect();
  if (boundaries.top > window.innerHeight - 168) {
    Listitem.classList.add("at-end-skill-container");
  } else {
    Listitem.classList.remove("at-end-skill-container");
  }

  data = data.sort((a, b) => a.length - b.length);

  Listitem.innerHTML = "";
  for (let i of data) {
    let li = document.createElement("span");
    li.textContent = i;
    Listitem.appendChild(li);
  }

  // Listid.appendChild(Listitem);
  Listitem.style.display = "flex";
  Listid.style.position = "relative";
};

toHideSkillContainer = function (id, item) {
  let Listid = document.getElementById(id);
  let Listitem = document.getElementById(item);
  // Listid.removeChild(Listitem);

  Listitem.addEventListener("mouseover", () => {
    // console.log(Listitem.getBoundingClientRect());
    Listitem.style.display = "flex";
    Listid.style.position = "relative";
    clearTimeout(interval);
  });

  Listitem.addEventListener("mouseout", () => {
    Listitem.style.display = "none";
    Listid.style.position = "";
  });

  interval = setTimeout(() => {
    Listitem.style.display = "none";
    Listid.style.position = "";
  }, 50);
};
function toShowData(data, method = "POST") {
  console.log(FilteringData.FetchedData);
  datalistItems.innerHTML = "";

  lst = [];
  if (data.length !== 0 && data[1] !== null) {
    TotalValue.textContent = data[0];
    data = data[1];
    console.log(data);
    let interval;
    for (let i in data) {
      let li = document.createElement("li");
      li.id = data[i].ResumeId;
      let FirstName = document.createElement("p");
      FirstName.textContent = data[i].FirstName;

      let Role = document.createElement("p");
      Role.textContent = data[i].Role;

      let SkillName = document.createElement("button");
      SkillName.id = i;
      SkillName.classList.add("SkillElement");
      SkillName.textContent = "Skills";

      SkillName.addEventListener("mouseover", () => {
        let values = data[i].SkillName;
        toUpdateSkillContainer(values, li.id, ul.id);
        ul.classList.remove("LocationContainer");

        clearTimeout(interval);
      });

      SkillName.addEventListener("mouseout", () => {
        toHideSkillContainer(li.id, ul.id);

        // ul.addEventListener("mouseover", () => {
        //   let values = data[i].SkillName;
        //   toUpdateSkillContainer(values, li.id, ul.id, interval);
        // });
      });

      let Experience = document.createElement("p");
      Experience.textContent = data[i].Experience + " Years";

      let Email = document.createElement("p");
      Email.textContent =
        data[i].Contact_Email !== "" ? data[i].Contact_Email : "abc@email.com";

      let Location = document.createElement("button");
      Location.id = i + "_Location";
      Location.classList.add("SkillElement");
      Location.classList.add("LocationElement");
      Location.textContent = "Locations";

      Location.addEventListener("mouseover", () => {
        let values =
          data[i].Location[0] === null ? ["Unknown"] : data[i].Location;
        toUpdateSkillContainer(values, li.id, ul.id);
        ul.classList.add("LocationContainer");
        clearTimeout(interval);
      });

      Location.addEventListener("mouseout", () => {
        toHideSkillContainer(li.id, ul.id);
      });
      // Location.textContent =
      //   data[i].Location[0] === null ? "Unknown" : data[i].Location;

      let Phone_no = document.createElement("p");
      Phone_no.textContent =
        data[i].Contact_Phone !== "" ? data[i].Contact_Phone : "XXXXXXXXXX";

      let UploadDate = document.createElement("p");
      UploadDate.textContent = data[i].UploadDate;

      let icon = document.createElementNS("http://www.w3.org/2000/svg", "svg");
      let useElement = document.createElementNS(
        "http://www.w3.org/2000/svg",
        "use"
      );
      useElement.setAttributeNS(
        "http://www.w3.org/1999/xlink",
        "href",
        "./Icons/icons.svg#ActionIcon"
      );

      icon.addEventListener("click", () => {
        li.classList.remove("RecentElements");
        updateView(li.id, true);
        fetchviewdata(li.id);
      });

      let ul = document.createElement("li");
      ul.id = "SkillsContainer" + i;
      ul.classList.add("SkillsContainer");

      icon.appendChild(useElement);
      li.appendChild(FirstName);
      li.appendChild(Role);
      li.appendChild(SkillName);
      li.appendChild(Experience);
      li.appendChild(Email);
      li.appendChild(Location);
      li.appendChild(Phone_no);
      li.appendChild(UploadDate);
      li.appendChild(icon);
      li.appendChild(ul);

      className =
        toCheckRecent(data[i].UploadDate) < 3 && !data[i].IsViewed
          ? "RecentElements"
          : "None";
      li.classList.add("elementStyle", className);
      datalistItems.appendChild(li);
      datalistItems.scrollTop = 0;
    }

    if (method === "GET") {
      Filterdata.ResumeIdList.ResumeIdValue.push({ ResumeIdValue: lst });
      console.log(Filterdata);
    }
  } else {
    TotalValue.textContent = data[0];
    let li = document.createElement("li");
    li.textContent = "No data";
    datalistItems.appendChild(li);
  }
  loader.style.display = "none";
}

// ***********************Pagination Code Start***********************************

function displayItems(data, page) {
  currentPage = page;
  paginationData = data;
  const startIndex = (page - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const newData =
    data[1] !== null
      ? Object.values(data[1]).sort((a, b) => b.ResumeId - a.ResumeId)
      : null;
  const pageItems =
    newData !== null ? newData.slice(startIndex, endIndex) : null;
  console.log("page items ", pageItems);
  if (currentPage === 1) {
    document.getElementById("previous-button").classList.add("ondisablebutton");
  } else {
    document
      .getElementById("previous-button")
      .classList.remove("ondisablebutton");
  }
  if (currentPage === Math.ceil(data[0] === 0 ? 1 : data[0] / itemsPerPage)) {
    document.getElementById("next-button").classList.add("ondisablebutton");
  } else {
    document.getElementById("next-button").classList.remove("ondisablebutton");
  }
  toShowData([data[0], pageItems]);

  const pageContainer = document.getElementById("page-number");
  pageContainer.textContent = `Page ${page} of ${Math.ceil(
    data[0] === 0 ? 1 : data[0] / itemsPerPage
  )}`;
}

function goToPreviousPage() {
  if (currentPage > 1) {
    currentPage--;
    displayItems(paginationData, currentPage);
  }
}

function goToNextPage() {
  if (
    currentPage <
    Math.ceil(Object.keys(paginationData[1]).length / itemsPerPage)
  ) {
    currentPage++;
    displayItems(paginationData, currentPage);
  }
}

function goToPage(page) {
  if (
    page >= 1 &&
    page <= Math.ceil(Object.keys(paginationData[1]).length / itemsPerPage)
  ) {
    currentPage = page;
    displayItems(paginationData, currentPage);
  }
}

// Attach event listeners
document
  .getElementById("previous-button")
  .addEventListener("click", goToPreviousPage);
document.getElementById("next-button").addEventListener("click", goToNextPage);
document.getElementById("jump-button").addEventListener("click", () => {
  const input = document.getElementById("jump-input");
  const pageNumber = parseInt(input.value);
  goToPage(pageNumber);
});

// ***********************Pagination Code End*************************************
// Check Recent

function toCheckRecent(data) {
  if (data) {
    const [day, month, year] = data.split("-").map(Number);
    const date1 = new Date(year, month - 1, day);
    const date2 = new Date();

    const differenceMs = Math.abs(date2 - date1);

    const differenceDays = Math.ceil(differenceMs / (1000 * 60 * 60 * 24));

    return differenceDays;
  }
}

// toCheckRecent("02-05-2024");
// toshowdata = async (data) => {
//   vale = {
//     data: data,
//   };
//   await fetch("http://localhost:8000/Resumeslist", {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json",
//     },
//     body: JSON.stringify(vale),
//   })
//     .then((response) => {
//       if (!response.ok) {
//         throw new Error("Network response was not ok");
//       }
//       return response.json();
//     })
//     .then((response) => console.log(response));
// };

// window.onload = () => {
//   document.addEventListener("DOMContentLoaded", function () {
//     console.log("Start");
//     getHtml();
//     console.log("End");
//   });
//   console.log(document.getElementById("SearchItems"));
// };
// window.onload = () => {
// document.addEventListener("DOMContentLoaded", function () {
//   // console.log("Start");
//   // getHtml();
//   // console.log("End");
//   console.log(document.getElementById("SearchFilters"));
// });
// };

// window.onload = async () => {
//   await getHtml();
//   console.log(document.getElementById("SearchItems"));
// };

// console.log(document.getElementById("SearchItems"));

// Experience

DropdownSelectFunction = (data) => {
  var listItems = data.getElementsByTagName("li");
  let lst = ["All", "0-1", "1-3", "3-5", "5-9", "9-50"];
  for (var i = 0; i < listItems.length; i++) {
    listItems[i].setAttribute("data-value", lst[i]);
    listItems[i].addEventListener("click", function () {
      let Value = document.getElementById(this.id).textContent;
      // let Experiencetitle = document.getElementById("ExperienceValue");

      // Experiencetitle.textContent = Value !== "All" ? Value : "Experience";
      ExperienceDropdownFunction();
      if (Value === "All") {
        ExperienceSearchHistory.innerHTML = "";
        Filterdata.Candidate.Experience = [];
        ExperienceSearchHistoryContainer.innerHTML = "";
        toapplyfilters(Filterdata);
      } else {
        const [start, end] = this.getAttribute("data-value")
          .split("-")
          .map(Number);
        let items = Filterdata.Candidate.Experience.find(
          (item) => item.Experience[0] === start && item.Experience[1] === end
        );

        if (!items) {
          let Unique_id = generateUniqueId();
          Filterdata.Candidate.Experience.push({
            uniqueId: Unique_id,
            Experience: [start, end],
          });

          toAppendHistory(Value, Unique_id, ExperienceSearchHistory);
          toapplyfilters(Filterdata);
        }
      }

      toCheckSearchHistory();
    });
  }
};

DateDropdownSelectFunction = (data) => {
  console.log(data);
  var listItems = data.getElementsByTagName("li");
  let lst = [
    "All",
    "1 days",
    "7 days",
    "30 days",
    "60 days",
    "180 days",
    "360 days",
  ];
  for (var i = 0; i < listItems.length; i++) {
    listItems[i].setAttribute("data-value", lst[i]);
    listItems[i].addEventListener("click", function () {
      Filterdata.Candidate.UploadDate = [];

      let Value = document.getElementById(this.id).textContent;
      let Datetitle = document.getElementById("DateValue");

      Datetitle.textContent = Value !== "All" ? Value : "Date";
      DateDropdownFunction();

      if (Value === "All") {
        Filterdata.Candidate.UploadDate = [];
        toapplyfilters(Filterdata);
      } else {
        const start = this.getAttribute("data-value").split(" ")[0];
        Filterdata.Candidate.UploadDate.push({
          uniqueId: generateUniqueId(),
          UploadDate: start,
        });

        console.log(Filterdata);
      }
      toapplyfilters(Filterdata);
    });
  }
};

setIds();
function setIds() {
  SearchFilters = document.getElementById("SearchFilters");
  TotalValue = document.getElementById("TotalValue");
  chatbot = document.getElementById("Chatbot");
  // SearchInput = document.getElementById("SearchInput");
  SearchItems = document.getElementById("SearchItems");
  SearchButton = document.getElementById("SearchButton");
  // listItems = document.getElementById("listItems");
  ExperienceList = document.getElementById("ExperienceList");
  DateList = document.getElementById("DateList");
  SkillSuggestions = document.getElementById("SkillSuggestions");
  LocationSuggestions = document.getElementById("LocationSuggestions");
  SuggestionContainer = document.getElementById("SuggestionContainer");
  LocationValue = document.getElementById("LocationValue");
  LocationSearchHistory = document.getElementById("LocationSearchHistory");
  SkillSearchHistory = document.getElementById("SkillSearchHistory");
  ExperienceSearchHistory = document.getElementById("ExperienceSearchHistory");
  SkillSearchHistorySpan = document.getElementById("SkillSearchHistory-span");
  LocationSearchHistorySpan = document.getElementById(
    "LocationSearchHistory-span"
  );
  ExperienceSearchHistorySpan = document.getElementById(
    "ExperienceSearchHistory-span"
  );
  SkillSearchHistoryContainer = document.getElementById(
    "SkillSearchHistory-Overflow"
  );
  LocationSearchHistoryContainer = document.getElementById(
    "LocationSearchHistory-Overflow"
  );
  ExperienceSearchHistoryContainer = document.getElementById(
    "ExperienceSearchHistory-Overflow"
  );

  console.log(SuggestionContainer);
  DropdownSelectFunction(ExperienceList);
  DateDropdownSelectFunction(DateList);

  // SearchFilters.addEventListener("keydown", function (event) {
  //   if (event.key === "Enter") {
  //     let value = event.target.value;
  //     value = value.split(",");
  //     for (let i of value) {
  //       const data = {
  //         uniqueId: generateUniqueId(),
  //         SkillName: i,
  //       };
  //       let li = document.createElement("li");
  //       li.textContent = i;
  //       li.id = data.uniqueId;
  //       li.onclick = function () {
  //         removeFunction(data.uniqueId);
  //       };
  //       SearchItems.appendChild(li);
  //       Filterdata.Skill.SkillName.push(data);
  //     }
  //     SearchFilters.value = "";
  //   }
  // });

  // SearchButton.addEventListener("click", function () {
  //   toget();
  //   console.log(Filterdata);
  //   listItems.innerHTML = "";
  // });
}

// adding skill function
function toSkillsclick(value) {
  value = value.trim();
  if (value === "More Skills") {
    toappendSkills(FilteringData.AllSkills);
    FilteringData.Skills = FilteringData.AllSkills;
  } else {
    let values = Filterdata.Skill.SkillName.find(
      (item) => item.SkillName === value
    );
    console.log(values);
    if (!values) {
      let Unique_id = generateUniqueId();
      Filterdata.Skill.SkillName.push({
        uniqueId: Unique_id,
        SkillName: value.toLowerCase(),
      });
      toAppendHistory(value, Unique_id, SkillSearchHistory);
      toCheckSearchHistory();
    }
    SkillDropdownFunction();
  }
}

toappendSkills = (data, value = false) => {
  console.log(data);
  SkillList.innerHTML = "";
  // data = data.SkillList !== undefined ? data.SkillList : data;
  data = data.sort((a, b) => a.localeCompare(b));
  if (value) {
    data.push("More Skills");
  }
  console.log(data);
  for (let i of data) {
    let li = document.createElement("li");
    li.textContent = i;
    li.id = i;
    li.setAttribute("data-value", i);
    li.addEventListener("click", () => {
      value = li.id;
      toSkillsclick(value);
      toapplyfilters(Filterdata);
      // toget();
    });
    SkillList.appendChild(li);
  }
  if (value) {
    SkillList.lastChild.classList.add("SKillFilterLastChild");
  }
};

// adding location function

function tolocationclick(value) {
  value = value.trim();
  if (value === "All") {
    LocationSearchHistory.innerHTML = "";
    Filterdata.WorkExperience.Location = [];
    LocationSearchHistoryContainer.innerHTML = "";
    toCheckSearchHistory();
    toapplyfilters(Filterdata);
  } else {
    let values = Filterdata.WorkExperience.Location.find(
      (item) => item.Location === value.toLowerCase()
    );
    console.log(values, value);
    if (!values) {
      Unique_id = generateUniqueId();
      toAppendHistory(value, Unique_id, LocationSearchHistory);

      Filterdata.WorkExperience.Location.push({
        uniqueId: Unique_id,
        Location: value.toLowerCase(),
      });
      console.log(Filterdata.WorkExperience);
      toCheckSearchHistory();
    }
  }
}
toappendLocation = (data) => {
  Locationlist.innerHTML = "";
  data = data.States !== undefined ? data.States : data;
  data = data.sort((a, b) => a.localeCompare(b));
  for (let i of data) {
    let li = document.createElement("li");

    li.textContent = i;
    li.id = i;
    li.setAttribute("data-value", i);
    li.addEventListener("click", () => {
      // LocationValue.textContent = li.id === "All" ? "Location" : li.id;
      value = li.id;
      tolocationclick(value);
      LocationdropdownFunction();
      // toget();
      toapplyfilters(Filterdata);
    });
    Locationlist.appendChild(li);
  }
};

FetchingLocation = () => {
  fetch("./assets/Data/SuggestionsList.json")
    .then((response) => response.json())
    .then((data) => {
      toappendLocation(data);
      // toappendSkills(data);
      FilteringData.LocationCities = [
        ...FilteringData.LocationCities,
        ...data.States,
      ];
      // FilteringData.Skills = [...data.SkillList];
    });
};

FetchingSkills = () => {
  const item = FilteringData.onSelectSubFolder;
  const value = FilteringData.onFolderValue;

  console.log(item, value);
  fetch("http://localhost:8000/fetch_folder_skills")
    .then((response) => response.json())
    .then((data) => {
      if (value === false) {
        toappendSkills([...new Set(Object.values(data).flat())]);
        FilteringData.Skills = [...new Set(Object.values(data).flat())];
      } else {
        if (data[item]) {
          toappendSkills(data[item], true);
          FilteringData.Skills = [...data[item]];
          FilteringData.AllSkills = [...new Set(Object.values(data).flat())];
        } else {
          toappendSkills([...new Set(Object.values(data).flat())]);
          FilteringData.Skills = [...new Set(Object.values(data).flat())];
        }
      }
    });
};
// let data = ;
FetchingSkills();
// Dropdowncode

(function () {
  downicon1 = document.getElementById("DownIcon1");
  downicon2 = document.getElementById("DownIcon2");
  downicon3 = document.getElementById("DownIcon3");
  downicon4 = document.getElementById("DownIcon4");
  Locationdropdown = document.getElementById("Locationdropdown");
  ExperienceDropdown = document.getElementById("ExperienceDropdown");
  SkillDropdown = document.getElementById("SkillDropdown");
  DateDropdown = document.getElementById("DateDropdown");
  LocationHeader = document.getElementById("Location-Header");
  ExperienceHeader = document.getElementById("Experience-Header");
  SkillHeader = document.getElementById("Skill-Header");
  DateHeader = document.getElementById("Date-Header");
  SkillList = document.getElementById("SkillList");
  SkillValue = document.getElementById("SkillValue");
  ExperienceMainContainer = document.getElementById("ExperienceMainContainer");
  viewsection = document.getElementById("viewsection");
  viewdatacloseicon = document.getElementById("viewdatacloseicon");
  viewdatadownloadicon = document.getElementById("viewdatadownloadicon");
})();

// to Close Other Functions

function tocloseAllOtherFunctions(item) {
  value = item.id.split("-")[0];
  if (Locationdropdown.style.display === "block" && value !== "Location") {
    LocationdropdownFunction();
  }
  if (ExperienceDropdown.style.display === "block" && value !== "Experience") {
    ExperienceDropdownFunction();
  }
  if (SkillDropdown.style.display === "block" && value !== "Skill") {
    SkillDropdownFunction();
  }
  if (DateDropdown.style.display === "block" && value !== "Date") {
    DateDropdownFunction();
  }
}

LocationdropdownFunction = () => {
  if (Locationdropdown.style.display === "block") {
    Locationdropdown.classList.remove("dropdownVisible");
    Locationdropdown.style.display = "none";
    downicon1.classList.remove("IconStyles");
    LocationHeader.style.boxShadow = "none";
  } else {
    LocationHeader.style.boxShadow = "0px 2px 2px 0px #f4f2ff";
    Locationdropdown.classList.add("dropdownVisible");
    Locationdropdown.style.display = "block";
    downicon1.classList.add("IconStyles");
    SearchLocation.value = "";
    FetchingLocation();
    tocloseAllOtherFunctions(LocationHeader);
  }
};
ExperienceDropdownFunction = () => {
  if (ExperienceDropdown.style.display === "block") {
    ExperienceDropdown.classList.remove("dropdownVisible");
    ExperienceDropdown.style.display = "none";
    downicon2.classList.remove("IconStyles");
    ExperienceHeader.style.boxShadow = "none";
  } else {
    ExperienceHeader.style.boxShadow = "0px 2px 2px 0px #f4f2ff";
    ExperienceDropdown.classList.add("dropdownVisible");
    ExperienceDropdown.style.display = "block";
    downicon2.classList.add("IconStyles");
    tocloseAllOtherFunctions(ExperienceHeader);
  }
};

SkillDropdownFunction = () => {
  if (SkillDropdown.style.display === "block") {
    SkillDropdown.classList.remove("dropdownVisible");
    SkillDropdown.style.display = "none";
    downicon3.classList.remove("IconStyles");
    SkillHeader.style.boxShadow = "none";
    document.getElementById("SearchSkills").value = "";
  } else {
    SkillHeader.style.boxShadow = "0px 2px 2px 0px #f4f2ff";
    SkillDropdown.classList.add("dropdownVisible");
    SkillDropdown.style.display = "block";
    downicon3.classList.add("IconStyles");
    FetchingSkills();
    tocloseAllOtherFunctions(SkillHeader);
  }
};

DateDropdownFunction = () => {
  if (DateDropdown.style.display === "block") {
    DateDropdown.classList.remove("dropdownVisible");
    DateDropdown.style.display = "none";
    downicon4.classList.remove("IconStyles");
    DateHeader.style.boxShadow = "none";
  } else {
    DateHeader.style.boxShadow = "0px 2px 2px 0px #f4f2ff";
    DateDropdown.classList.add("dropdownVisible");
    DateDropdown.style.display = "block";
    downicon4.classList.add("IconStyles");
    tocloseAllOtherFunctions(DateHeader);
  }
};

LocationHeader.addEventListener("click", LocationdropdownFunction);
ExperienceHeader.addEventListener("click", ExperienceDropdownFunction);
SkillHeader.addEventListener("click", SkillDropdownFunction, true);
DateHeader.addEventListener("click", DateDropdownFunction);
// toPreventDefault(LocationHeader);
// toPreventDefault(SkillHeader);
// toPreventDefault(ExperienceHeader);
// toPreventDefault(DateHeader);

function toPreventDefault(id) {
  console.log(Array.from(id.children));
  Array.from(id.children).forEach((item) => {
    item.addEventListener("click", (event) => {
      event.stopPropagation();
    });
  });
}
window.addEventListener("click", function (event) {
  if (!event.target.closest(".Datasection-MainPlusDropDropDown")) {
    if (
      SkillDropdown.style.display === "block" &&
      event.target.textContent !== "More Skills"
    ) {
      SkillDropdownFunction();
    }
    if (ExperienceDropdown.style.display === "block") {
      ExperienceDropdownFunction();
    }
    if (Locationdropdown.style.display === "block") {
      LocationdropdownFunction();
    }
    if (DateDropdown.style.display === "block") {
      DateDropdownFunction();
    }
  }
});

// SkillHeader.addEventListener("blur", () => {
//   let interval = setTimeout(() => {
//     SkillDropdownFunction();
//   }, 100);
//   SkillDropdown.addEventListener("mouseenter", () => {
//     clearTimeout(interval);
//   });
//   SkillDropdown.addEventListener("mouseleave", SkillDropdownFunction);
// });

FetchingLocation();

//  Fetching All Cities

FetchCities = async () => {
  let response = await fetch(
    "https://countriesnow.space/api/v0.1/countries/cities",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        country: "India",
      }),
    }
  );
  let data = await response.json();

  FilteringData.LocationCities = [
    ...FilteringData.LocationCities,
    ...data.data,
  ];
};

FetchCities();

// Search Location Functionality
SearchLocation = document.getElementById("SearchLocation");
SearchLocation.addEventListener("input", (event) => {
  data = FilteringData.LocationCities.filter((item) =>
    item.toLowerCase().includes(event.target.value.toLowerCase())
  );
  data = new Set(data);
  toappendLocation([...data]);
  if ([...data].length === 0) {
    toappendLocation([event.target.value]);
  }
});

SearchLocation.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && event.target.value.length > 0) {
    tolocationclick(event.target.value);
    toapplyfilters(Filterdata);
    SearchLocation.value = "";
    FetchingLocation();
  }
});

// Append Location by input

// SearchLocation.addEventListener("keydown", (event) => {
//   if (event.target.value.length > 0 && event.key === "Enter") {
//     let values = Filterdata.WorkExperience.Location.find(
//       (item) => item.Location === event.target.value.toLowerCase()
//     );
//     console.log(values, event.target.value);
//     if (!values) {
//       Unique_id = generateUniqueId();
//       toAppendHistory(event.target.value, Unique_id, LocationSearchHistory);

//       Filterdata.WorkExperience.Location.push({
//         uniqueId: Unique_id,
//         Location: li.id.toLowerCase(),
//       });
//       console.log(Filterdata.WorkExperience);
//       toCheckSearchHistory();
//     }
//   }
//   LocationdropdownFunction();
//   // toget();
//   toapplyfilters(Filterdata);
//   Locationlist.appendChild(li);
// });

// Append Loaction History

LocationSearchHistory = document.getElementById("LocationSearchHistory");

removeFunction = (id, item) => {
  const para1 = document.getElementById(id);
  para1.parentNode.removeChild(para1);

  if (item.id === "LocationSearchHistory") {
    Filterdata.WorkExperience.Location =
      Filterdata.WorkExperience.Location.filter((item) => item.uniqueId !== id);
  } else if (item.id === "ExperienceSearchHistory") {
    Filterdata.Candidate.Experience = Filterdata.Candidate.Experience.filter(
      (item) => item.uniqueId !== id
    );
  } else {
    Filterdata.Skill.SkillName = Filterdata.Skill.SkillName.filter(
      (item) => item.uniqueId !== id
    );
    console.log(Filterdata.Skill.SkillName);
  }

  toapplyfilters(Filterdata);
  toShowMoreApplyFilters(item);
  toCheckSearchHistory();
};

function toAppendHistory(data, id, list) {
  let li = document.createElement("li");
  let p = document.createElement("p");
  p.textContent = data;
  li.appendChild(p);

  let span = document.createElement("span");
  span.textContent = " X ";
  li.appendChild(span);

  li.id = id;
  li.addEventListener("click", () => {
    removeFunction(li.id, list);
    toCheckSearchHistory();
  });
  list.appendChild(li);
  toShowMoreApplyFilters(list);
}

//  Search History
SearchHistoryContainer = document.getElementById("SearchHistoryContainer");

function toCheckSearchHistory() {
  let LocationHistory = Filterdata.WorkExperience.Location.length;
  let SkillHistory = Filterdata.Skill.SkillName.length;
  let ExperienceHistory = Filterdata.Candidate.Experience.length;

  if (LocationHistory + ExperienceHistory + SkillHistory === 0) {
    SearchHistoryContainer.style.display = "none";
  } else {
    SearchHistoryContainer.style.display = "grid";
  }
}

toCheckSearchHistory();

// Clear History
function ClearHistory() {
  Filterdata.WorkExperience.Location = [];
  Filterdata.Skill.SkillName = [];
  Filterdata.Candidate.Experience = [];
  LocationSearchHistory.innerHTML = "";
  SkillSearchHistory.innerHTML = "";
  ExperienceSearchHistory.innerHTML = "";
  SearchHistoryContainer.style.display = "none";
  SkillSearchHistoryContainer.innerHTML = "";
  ExperienceSearchHistoryContainer.innerHTML = "";
  LocationSearchHistoryContainer.innerHTML = "";
  toClearAllSubFilter();
  // toget();
  toapplyfilters(Filterdata);
}

document.getElementById("ClearHistory").addEventListener("click", ClearHistory);

// Search Skills

document
  .getElementById("SearchSkills")
  .addEventListener("input", function (event) {
    data = FilteringData.Skills.filter((item) =>
      item.toLowerCase().includes(event.target.value.toLowerCase())
    );
    toappendSkills(data);
    if (data.length === 0) {
      toappendSkills([event.target.value]);
    }
  });

// Search Skills by Enter
document
  .getElementById("SearchSkills")
  .addEventListener("keydown", function (event) {
    if (event.key === "Enter" && event.target.value.length > 0) {
      toSkillsclick(event.target.value);
      document.getElementById("SearchSkills").value = "";
      FetchingSkills();
      toapplyfilters(Filterdata);
    }
  });
// toapplyFilters

toapplyfilters = (data) => {
  data = tocheck(data);
  let sampleData = FilteringData.FetchedData;
  for (let key in data) {
    if (data[key]["check"].length > 0 && key !== "ResumeIdList") {
      for (let i of data[key]["check"]) {
        if (i === "FirstName") {
          sampleData = sampleData.filter((item) => {
            if (item["FirstName"].toLowerCase().includes(data[key][i])) {
              return true;
            }
            return false;
          });
        } else if (i === "Location") {
          sampleData = sampleData.filter((item) => {
            return data[key][i].some((item2) => {
              if (item["Location"][0] !== null) {
                return item["Location"].some((location) => {
                  return location.toLowerCase().includes(item2.toLowerCase());
                });
              }
            });
          });

          // if (
          //   data[key][i].some((item2) => {
          //     console.log(
          //       item["Location"]
          //         .join(",")
          //         .toLowerCase()
          //         .includes(item2.toLowerCase())
          //     );

          //     return item["Location"]
          //       .join(",")
          //       .toLowerCase()
          //       .includes(item2.toLowerCase());
          //   })
          // )
          //   return true;
          // else {
          //   return false;
          // }
        } else if (i === "Experience") {
          sampleData = sampleData.filter((item) => {
            let status = false;
            for (let j of data[key][i]) {
              if (
                parseFloat(item["Experience"]) >= parseFloat(j.slice(0, 1)) &&
                parseFloat(item["Experience"]) < parseFloat(j.slice(-1))
              ) {
                status = true;
              }
            }
            return status;
          });
        } else if (i === "SkillName") {
          sampleData = sampleData.filter((item) => {
            var ids = item["SkillName"].filter(
              (item2) => data[key][i].indexOf(item2.toLowerCase()) !== -1
            );
            if (ids.length === data[key][i].length) {
              return true;
            } else {
              return false;
            }
          });
        } else if (i === "UploadDate") {
          sampleData = sampleData.filter((item) => {
            if (
              tocheckUploadDate(item["UploadDate"]) < parseInt(data[key][i][0])
            ) {
              return true;
            } else {
              return false;
            }
          });
          console.log(sampleData);
        }
        // toShowData([sampleData.length, sampleData]);
      }
    }
  }
  FilteringData.TemporaryData = sampleData;
  // toShowData([sampleData.length, sampleData]);
  displayItems(
    [FilteringData.TemporaryData.length, FilteringData.TemporaryData],
    1
  );
};

// Upload date filter

function tocheckUploadDate(date) {
  if (date) {
    const [day, month, year] = date.split("-").map(Number);
    let date1 = new Date(year, month - 1, day);
    let date2 = new Date();
    let difference = date2.getTime() - date1.getTime();
    let days = Math.floor(difference / (1000 * 60 * 60 * 24));
    return days;
  }
}

// fetch resume

fetchviewdata = async (id) => {
  let data = "";
  let idvalue = {
    fileID: id,
  };
  let url = new URL("http://localhost:8000/view-resume");
  url.search = new URLSearchParams(idvalue).toString();
  let response = await fetch(url);
  data = await response.json();
  if (data) {
    console.log(data);

    const [type, link] = getFileViewerUrl(data);
    console.log(link);

    if (type == 1) {
      const imageSrc = link;
      const iframeContent = `
              <!DOCTYPE html>
              <html lang="en">
              <head>
                  <meta charset="UTF-8">
                  <meta name="viewport" content="width=device-width, initial-scale=1.0">
                  <title>Image</title>
                  <style>
                      body, html {
                          margin: 0;
                          padding: 0;
                          height: 100%;
                          display: flex;
                          align-items: center;
                          justify-content: center;
                      }
                      .image-container {
                          display: flex;
                          align-items: center;
                          justify-content: center;
                          height: 100vh; /* Ensure it takes full height */
                      }
                      img {
                          max-width: 100%;
                          max-height: 100%;
                          object-fit: contain; /* Adjust as needed */
                      }
                  </style>
              </head>
              <body>
                  <div class="image-container">
                      <img src="${imageSrc}" alt="Centered Image">
                  </div>
              </body>
              </html>
          `;

      // Create a Blob from the iframe content
      const blob = new Blob([iframeContent], { type: "text/html" });
      // Create an object URL from the Blob
      const url = URL.createObjectURL(blob);

      viewcandidatedata.src = url;
    } else {
      viewcandidatedata.src = link;
    }

    viewsection.style.display = "flex";


    try {
      let response;
      if (type == 2) {
        response = await fetch(data);
      } else {
        response = await fetch(link);
      }

      const blob = await response.blob();

      const url = window.URL.createObjectURL(blob);
      document.getElementById("viewdatadownloadiconA").href = url;
      viewdatadownloadiconA.download = "resume";
    } catch (error) {
      throw Error(error.message);
    }


  }

};

function getFileViewerUrl(fileUrl) {
  const decodedUrl = decodeURIComponent(fileUrl);
  const fileExtension = getFileExtension(decodedUrl);

  switch (fileExtension) {
    case "pdf":
      return [0, fileUrl];
    case "doc":
    case "docx":
      return [
        2,
        `https://view.officeapps.live.com/op/embed.aspx?src=${encodeURIComponent(
          fileUrl
        )}`,
      ];
    case "jpg":
      // alert("File type is a jpg!");
      return [1, fileUrl];
    case "jpeg":
      // alert("File type is a jpeg!");
      return [1, fileUrl];
    case "png":
      // alert("File type is a png!");
      return [1, fileUrl];
    default:
      alert("File type not supported!");
      return "";
  }
}

function getFileExtension(url) {
  const parts = url.split(".");
  if (parts.length > 1) {
    return parts.pop().toLowerCase().split("?")[0];
  }
  return "";
}

// close viewdata

viewdatacloseicon.addEventListener("click", () => {
  viewsection.style.display = "none";
  document.getElementById("viewcandidatedata").src = "";
});

// sort by uploaddate

function sortByUpload(a, b) {
  dateA = new Date(a.UploadDate.split("-").reverse().join("-"));
  dateB = new Date(b.UploadDate.split("-").reverse().join("-"));
  console.log(sortedorder, sortedordervalue);
  if (dateA > dateB) {
    return 1 * sortedordervalue;
  } else if (dateA < dateB) {
    return -1 * sortedordervalue;
  }
  return 0;
}

document.getElementById("DatasortUpdateDate").addEventListener("click", () => {
  if (sortedorder === "asc") {
    sortedordervalue = 1;
    sortedorder = "desc";
  } else {
    sortedordervalue = -1;
    sortedorder = "asc";
  }
  FilteringData.TemporaryData = FilteringData.TemporaryData.sort(sortByUpload);
  // FilteringData.TemporaryData = FilteringData.FetchedData;
  displayItems(
    [FilteringData.TemporaryData.length, FilteringData.TemporaryData],
    1
  );
});

// show modal

document.getElementById("uploadresumes").onclick = () => {
  dialog.showModal();
};

document.getElementById("perPageRecords").addEventListener("change", () => {
  itemsPerPage = document.getElementById("perPageRecords").value;
  displayItems(
    [FilteringData.TemporaryData.length, FilteringData.TemporaryData],
    1
  );
});

document
  .getElementById("searchbyname")
  .addEventListener("input", function (event) {
    Filterdata.Candidate.FirstName = [{ FirstName: event.target.value }];
    toapplyfilters(Filterdata);
  });

//  Update View

async function updateView(id, view) {
  data = {
    id: id,
    isviewed: view,
  };

  let response = await fetch("http://localhost:8000/Isviewed", {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  return await response.json();
}

// Filter Add More

function toShowMoreApplyFilters(valueid) {
  let hiddenitemContainer = document.getElementById(`${valueid.id}-Overflow`);
  let hiddenitemValue = document.getElementById(`${valueid.id}-span`);

  if (valueid.scrollWidth > valueid.clientWidth) {
    // hiddenitemContainer.style.display = "flex";
    hiddenitemValue.style.display = "block";
    let OverflowItem = valueid.removeChild(valueid.lastChild);
    hiddenitemContainer.appendChild(OverflowItem);
    hiddenitemValue.textContent = "+" + hiddenitemContainer.children.length;
    // alert("+" + hiddenItems);
  } else {
    if (hiddenitemContainer.children.length > 0) {
      let OverflowItem = hiddenitemContainer.removeChild(
        hiddenitemContainer.lastChild
      );
      valueid.appendChild(OverflowItem);

      if (valueid.scrollWidth > valueid.clientWidth) {
        // hiddenitemContainer.style.display = "flex";
        hiddenitemValue.style.display = "block";
        let OverflowItem = valueid.removeChild(valueid.lastChild);
        hiddenitemContainer.appendChild(OverflowItem);
        hiddenitemValue.textContent = "+" + hiddenitemContainer.children.length;
      } else {
        if (hiddenitemContainer.childNodes.length === 0) {
          hiddenitemContainer.style.display = "none";
          hiddenitemValue.style.display = "none";
        }
        // alert("-" + hiddenItems);
      }
      hiddenitemValue.textContent = "+" + hiddenitemContainer.children.length;
    } else {
      hiddenitemContainer.style.display = "none";
      hiddenitemValue.style.display = "none";
    }
  }
}

SkillSearchHistorySpan.addEventListener("mouseover", () => {
  SkillSearchHistoryContainer.style.display = "flex";
});

SkillSearchHistorySpan.addEventListener("mouseleave", () => {
  VisibleTimout = setTimeout(() => {
    SkillSearchHistoryContainer.style.display = "none";
  }, 280);
});

LocationSearchHistorySpan.addEventListener("mouseover", () => {
  LocationSearchHistoryContainer.style.display = "flex";
});

LocationSearchHistorySpan.addEventListener("mouseleave", () => {
  VisibleTimout = setTimeout(() => {
    LocationSearchHistoryContainer.style.display = "none";
  }, 280);
});
ExperienceSearchHistorySpan.addEventListener("mouseover", () => {
  ExperienceSearchHistoryContainer.style.display = "flex";
});
ExperienceSearchHistorySpan.addEventListener("mouseleave", () => {
  VisibleTimout = setTimeout(() => {
    ExperienceSearchHistoryContainer.style.display = "none";
  }, 280);
});

function toClearAllSubFilter() {
  SkillSearchHistoryContainer.style.display = "none";
  LocationSearchHistoryContainer.style.display = "none";
  ExperienceSearchHistoryContainer.style.display = "none";
  SkillSearchHistorySpan.style.display = "none";
  LocationSearchHistorySpan.style.display = "none";
  ExperienceSearchHistorySpan.style.display = "none";
}

containers = [
  SkillSearchHistoryContainer,
  LocationSearchHistoryContainer,
  ExperienceSearchHistoryContainer,
];

containers.forEach((container) => {
  container.addEventListener("mouseleave", () => {
    container.style.display = "none";
  });

  container.addEventListener("mouseover", () => {
    clearTimeout(VisibleTimout);
  });
});

// toBack Page

BackArrow.onclick = async () => {
  FilteringData.page = "main";
  Filterdata.Candidate.UploadDate = [];
  Filterdata.Skill.SkillName = [];
  Filterdata.WorkExperience.Location = [];
  Filterdata.Candidate.Experience = [];
  FilteringData.TemporaryData = [];
  FilteringData.onFolderValue = false;
  FilteringData.onSelectSubFolder = "";
  // FilteringData.onFolderSelect = "";
  await triggerDOMContentLoaded();
};
