// let downicon1 = document.getElementById("DownIcon1");
// let downicon2 = document.getElementById("DownIcon2");
// let Locationdropdown = document.getElementById("Locationdropdown");
// let ExperienceDropdown = document.getElementById("ExperienceDropdown");
// let ExperienceHeader = document.getElementById("Experience-Header");

// let LocationdropdownFunction = () => {
//   if (Locationdropdown.style.display === "block") {
//     Locationdropdown.classList.remove("dropdownVisible");
//     Locationdropdown.style.display = "none";
//     downicon1.classList.remove("IconStyles");
//   } else {
//     Locationdropdown.classList.add("dropdownVisible");
//     Locationdropdown.style.display = "block";
//     downicon1.classList.add("IconStyles");
//   }
// };
// let ExperienceDropdownFunction = () => {
//   if (ExperienceDropdown.style.display === "block") {
//     ExperienceDropdown.classList.remove("dropdownVisible");
//     ExperienceDropdown.style.display = "none";
//     downicon2.classList.remove("IconStyles");
//   } else {
//     ExperienceDropdown.classList.add("dropdownVisible");
//     ExperienceDropdown.style.display = "block";
//     ExperienceDropdown.style.right = "12%";
//     downicon2.classList.add("IconStyles");
//   }
// };
// downicon1.addEventListener("click", LocationdropdownFunction);
// downicon2.addEventListener("click", ExperienceDropdownFunction);
// ExperienceHeader.addEventListener("click", ExperienceDropdownFunction);

(function () {
  MainSuggestionData = {
    MainFolders: [],
    SubCategoriesData: [],
  };
  SubCategoriesSuggestions = document.getElementById(
    "SubCategoriesSuggestions"
  );
  SearchFilters = document.getElementById("SearchFilters");
  Logo = document.getElementById("Logo");
  clearsearchvalue = document.getElementById("ClearSearchValue");
})();

// SubCategories

// let clickedButton = "";

toAppendSuggestionData = (data) => {
  data = data.sort((a, b) => a.localeCompare(b));
  SubCategoriesSuggestions.innerHTML = "";
  for (let i of data) {
    let li = document.createElement("li");
    li.textContent = i;
    li.id = i;
    li.addEventListener("click", () => {
      let value = SearchFilters.value.split(" ");
      newvalue = value.slice(0, value.length - 1);
      // console.log(newvalue);
      newvalue.push(li.textContent);
      SearchFilters.value = newvalue.join(" ");
      SearchFilters.focus();
      // if (value.lastIndexOf("and") !== -1) {
      //   newvalue = value.slice(0, value.lastIndexOf("and") + 1);
      //   newvalue.push(li.textContent);
      //   SearchFilters.value = newvalue.join(" ");
      //   SearchFilters.focus();
      // } else if (value.lastIndexOf("and") === -1) {
      //   SearchFilters.value = li.textContent;
      //
      // }
      // console.log(SearchFilters.value);
      // items = items.find((item) => item.id === "Search" + li.id);
      // if (!items) {
      //   toAppendSearchItems(li.textContent);
      //   toDisplayClear();
      // }
    });
    SubCategoriesSuggestions.appendChild(li);
  }
};

// // remove SearchItem

// SearchremoveFunction = (data) => {
//   let li = document.getElementById(data);
//   li.remove();
//   toDisplayClear();
// };

// // Append Search History
// let SearchItems = document.getElementById("SearchItems");

// toAppendSearchItems = (data) => {
//   let li = document.createElement("li");
//   li.textContent = data;
//   li.id = "Search" + data;

//   let icon = document.createElementNS("http://www.w3.org/2000/svg", "svg");
//   icon.setAttribute("width", "12");
//   icon.setAttribute("height", "12");
//   let circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
//   circle.setAttribute("cx", "6");
//   circle.setAttribute("cy", "6");
//   circle.setAttribute("r", "6");
//   circle.setAttribute("fill", "white");
//   icon.appendChild(circle);
//   icon.style.marginLeft = "0.4rem";
//   li.addEventListener("click", () => {
//     SearchremoveFunction(li.id);
//   });
//   li.appendChild(icon);
//   SearchItems.appendChild(li);
// };

FetchingSubcategories = () => {
  fetch("http://localhost:8000/fetch_folder_subfolders")
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      MainSuggestionData.SubCategoriesData = Object.values(data).flat();
      toAppendSuggestionData(Object.values(data).flat());
    });
};

FetchingMainCategories = () => {
  fetch("./assets/Data/MainCategories.json")
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      MainSuggestionData.MainFolders = data.AllMainCategory;
    });
};
FetchingMainCategories();

// SuggestionContainer
HoverSuggestionListContainer = () => {
  if (
    SearchFilters.value.split(" ").slice(-1)[0].trim() !== "" &&
    SearchFilters.value.length > 0 &&
    SubCategoriesSuggestions.innerHTML !== ""
  ) {
    SuggestionContainer.style.display = "block";
    console.log(SubCategoriesSuggestions.innerHTML);
  } else {
    SuggestionContainer.style.display = "none";
  }
};
HideHoverSuggestionListContainer = () => {
  setTimeout(() => {
    SuggestionContainer.style.display = "none";
    // SearchFilters.value = "";
  }, 280);
};
FetchingSubcategories();

// Search Filter

SearchFilters.addEventListener("focus", HoverSuggestionListContainer);
SearchFilters.addEventListener("blur", HideHoverSuggestionListContainer);

SearchFilters.addEventListener("input", function (event) {
  if (event.target.value.length > 0) {
    SubCategoriesSuggestions.innerHTML = "";
    clearsearchvalue.style.display = "block";
    // let targetvalue = event.target.value;
    let inputvalue = event.target.value.split(" ");
    console.log(inputvalue);
    targetvalue = inputvalue.slice(-1)[0];
    data = MainSuggestionData.SubCategoriesData.filter((item) =>
      item.toLowerCase().includes(targetvalue.trim().toLowerCase())
    );

    if (data.length == 0) {
      SuggestionContainer.style.display = "none";
      SubCategoriesSuggestions.innerHTML = "";
    } else {
      SuggestionContainer.style.display = "block";
      toAppendSuggestionData(data);
    }
  } else {
    clearsearchvalue.style.display = "none";
    SuggestionContainer.style.display = "none";
  }
});

SearchFilters.addEventListener("keydown", function (event) {
  if (event.key === "Enter" && event.target.value.length > 0) {
    onSubmiting();
  }
});

// searchButton

function customSplit(line) {
  var pattern = /[,]|and|or/g;
  var splitline = line.split(pattern);
  splitline = splitline.filter((word) => word.trim().length > 0);
  return splitline;
}

// functionality
async function onSubmiting() {
  SearchFilters.blur();
  let value = SearchFilters.value.replace(/\s+/g, " ").trim();
  console.log(customSplit(value));
  let checkvalue = value.toLowerCase();
  for (i of MainSuggestionData.SubCategoriesData) {
    checkvalue = checkvalue.replace(i.toLowerCase(), "");
  }
  console.log(customSplit(checkvalue));
  if (customSplit(checkvalue).length === 0) {
    FilteringData.onFolderValue = true;
    FilteringData.onSelectSubFolder = customSplit(value)
      .join(" & ")
      .replace(/\s+/g, " ")
      .trim();
    FilteringData.chatbotData = false;
  } else {
    FilteringData.onFolderValue = false;
    FilteringData.onSelectSubFolder = value;

    FilteringData.chatbotData = false;
  }
  if (value.length > 0) {
    FilteringData.page = "data";
    await triggerDOMContentLoaded();
  }

  // SearchItems.innerHTML = "";
}

SearchButton.addEventListener("click", () => {
  if (SearchFilters.value.length > 0) {
    onSubmiting();
  }
});

// // ClearFunction
// let ClearFunction = document.getElementById("ClearFunction");

// ClearFunction.addEventListener("click", function () {
//   SearchItems.innerHTML = "";
//   toDisplayClear();
// });

// ClearDisplay
// function toDisplayClear() {
//   let Header_SearchItemsContainer = document.getElementById(
//     "Header_SearchItemsContainer"
//   );
//   let Value = SearchItems.childNodes;
//   if (Value.length > 0) {
//     Header_SearchItemsContainer.style.display = "flex";
//   } else {
//     Header_SearchItemsContainer.style.display = "none";
//   }
// }
// toDisplayClear();

// Logout
function Logout() {
  window.location.replace("index.html");
  setCookie(localStorage.getItem("Rsession_name"), " ", -1);
  localStorage.removeItem("Rsession_name");
  if (sessionStorage.getItem("data") != null) {
    sessionStorage.removeItem("data");
  }
}

// Logo

Logo.addEventListener("click", async function () {
  FilteringData.page = "main";
  Filterdata.Candidate.UploadDate = [];
  Filterdata.Skill.SkillName = [];
  Filterdata.WorkExperience.Location = [];
  Filterdata.Candidate.Experience = [];
  FilteringData.TemporaryData = [];
  FilteringData.onFolderValue = false;
  FilteringData.onSelectSubFolder = "";
  FilteringData.onFolderSelect = "";
  await triggerDOMContentLoaded();
});

// clear serach value

clearsearchvalue.addEventListener("click", function () {
  clearsearchvalue.style.display = "none";
  SearchFilters.value = "";
  SearchFilters.focus();
});
