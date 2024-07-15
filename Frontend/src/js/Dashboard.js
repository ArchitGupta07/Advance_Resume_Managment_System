(function () {
  containerList = document.getElementById("ContainerList");
  Categorysvalue = document.getElementById("Categorys");
  SubCategoryHeadingValue = document.getElementById("SubCategoryHeadingValue");
  SubCategoryHeading = document.getElementById("SubCategoryHeading");
  SubContainerList = document.getElementById("SubContainerList");
  SubCategorySection = document.getElementById("SubCategorySection");
  CloseSubContainer = document.getElementById("CloseSubContainer");
  AddFolderSkills = document.getElementById("AddFolderSkills");
  AddFolderName = document.getElementById("AddFolderName");
  AddFolderDisplayId = document.getElementById("AddFolderDisplayId");
  EditFolderDisplayId = document.getElementById("EditFolderDisplayId");
  EditFolderName = document.getElementById("EditFolderName");
  PreviousFolderName = document.getElementById("PreviousFolderName");
  ClearSubFolderSearchValue = document.getElementById(
    "ClearSubFolderSearchValue"
  );
  SubCategorySearchFilters = document.getElementById(
    "SubCategorySearchFilters"
  );
  UploadResumes = document.getElementById("UploadResumes");
  dialog = document.getElementById("dialog");
})();

// Category and SubCategory Data

Folders = {
  MainCategory: "",
  SubCategory: "",
};

// Filter Api JSon

// const Filterdata = {
//   Candidate: {
//     check: [],
//     FirstName: [],
//     LastName: [],
//     experience: [],
//   },

//   WorkExperience: {
//     check: [],
//     Location: [],
//   },

//   Education: {
//     check: [],
//     Degree: [],
//     Score: [],
//     YearOfPassing: [],
//     Branch: [],
//     Institution: [],
//   },
//   Contact: {
//     check: [],
//     Contact_type: [],
//     Contact_value: [],
//   },
//   Skill: {
//     check: [],
//     // SkillName: ["Java", "Python"],
//     SkillName: [],
//   },
//   ResumeIdList: {
//     check: [],
//     ResumeIdValue: [],
//   },
// };

// UniqueId
function generateUniqueId() {
  const randomNumber = Math.random().toString(16).slice(2);
  const timestamp = Date.now().toString(16);
  const uniqueId = timestamp + randomNumber;
  return uniqueId;
}

// Remove Function
// removeFunction = (id) => {
//   const para1 = document.getElementById(id);
//   console.log(para1);
//   para1.parentNode.removeChild(para1);
//   Filterdata.Skill.SkillName = Filterdata.Skill.SkillName.filter(
//     (item) => item.uniqueId !== id
//   );
// };

toDataPage = async (value) => {
  // window.location.href = url;
  if (
    MainSuggestionData.SubCategoriesData.find(
      (item) => item.toLowerCase() === value.toLowerCase()
    )
  ) {
    FilteringData.onSelectSubFolder = value;
    FilteringData.onFolderValue = true;
  } else {
    FilteringData.onSelectSubFolder = value;
    FilteringData.onFolderValue = false;
  }

  FilteringData.chatbotData = false;
  FilteringData.page = "data";
  await triggerDOMContentLoaded();
  // document.addEventListener("DOMContentLoaded", async () => {
  //   await getContentHtml(url);
  // });
  // await ;
};

createListitems = (data, List, functions, flagvalue, value = undefined) => {
  console.log(flagvalue);
  let li = document.createElement("li");
  li.classList.add("listItem");
  let MainDiv = document.createElement("div");

  for (let i = 0; i < 2; i++) {
    let idValue =
      i == 0 ? "./Icons/icons.svg#categoryicon" : "./Icons/icons.svg#EditIcon";
    let classValue = i == 0 ? "DashboardFolderIcon" : "DashboardFolderIcon2";
    let icon = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    let div = document.createElement("div");
    let useElement = document.createElementNS(
      "http://www.w3.org/2000/svg",
      "use"
    );
    useElement.setAttributeNS("http://www.w3.org/1999/xlink", "href", idValue);
    icon.appendChild(useElement);
    div.appendChild(icon);
    // icon.setAttribute("class", iconClass);
    div.setAttribute("class", classValue);
    if (!MainSuggestionData.MainFolders.includes(data) && i != 0) {
      div.classList.add("DashboardFolderIconallowed");
      div.onclick = (event) => {
        event.stopPropagation();
        // alert("You are not allowed to edit this folder");
        EditCategory(data);
      };
    }
    MainDiv.appendChild(div);
  }

  let div = document.createElement("div");
  div.classList.add("listContentContainer");

  let h4 = document.createElement("h4");
  // icon.setAttribute("class", "DashboardFolderIcon");

  h4.textContent = data;
  div.appendChild(h4);

  if (flagvalue[data] !== 0) {
    let createspan = document.createElement("span");
    createspan.textContent = `${flagvalue[data]} Just Added`;
    createspan.classList.add("Justadded");
    div.appendChild(createspan);
  } else {
    let createspan = document.createElement("span");
    createspan.textContent = ``;
    // createspan.classList.add("Justadded");
    createspan.style.height = "17.8px";
    div.appendChild(createspan);
  }

  li.appendChild(MainDiv);
  li.appendChild(div);
  li.id = i;
  li.addEventListener("click", () => {
    functions(data);
    if (value) {
      getFlag();
    }
  });
  List.append(li);
};

toDisplayFloder = (data) => {
  containerList.innerHTML = "";
  Categorysvalue.textContent = Object.keys(data).length;
  for (i of Object.keys(data)) {
    createListitems(i, containerList, toShowSubCategory, data);
  }
  tomodal();
};

function tomodal() {
  if (FilteringData.onFolderSelect !== "") {
    SubCategorySection.style.display = "flex";
    toShowSubCategory(FilteringData.onFolderSelect);
  } else {
    SubCategorySection.style.display = "none";
  }
}

toShowSubCategory = (id) => {
  if (id === "All Resumes") {
    toDataPage("Show All Resumes");
  } else {
    SubCategoryHeading.textContent = id;
    SubCategorySection.style.display = "flex";
    SubContainerList.innerHTML = "";
    // document.getElementById("Dashboard").style.overflow = "hidden";
    FilteringData.onFolderSelect = id;
    togetSubcategory(id);
  }
};

togetSubcategory = async (data) => {
  data = {
    category: data,
  };
  let url = new URL("http://localhost:8000/subCategoryflag/");
  url.search = new URLSearchParams(data).toString();
  await fetch(url, {
    method: "GET",
  })
    .then((response) => response.json())
    .then((responseData) => {
      Folders.SubCategory = responseData;
      toDisplaySubCategory(responseData);
    });
};

// SubCategory

toDisplaySubCategory = (data) => {
  console.log(Object.keys(data));
  SubContainerList.innerHTML = "";
  SubCategoryHeadingValue.textContent = Object.keys(data).length;
  for (let i of Object.keys(data)) {
    createListitems(i, SubContainerList, togetdata, data, "Sub Folder");
  }
};

function togetdata(id) {
  toDataPage(id);
  document
    .querySelectorAll("li")
    .forEach((li) => li.classList.remove("ContainerListactive"));
}

togetFolders = async () => {
  let url = new URL("http://localhost:8000/CategoryFlag");
  await fetch(url, {
    method: "GET",
  })
    .then((response) => response.json())
    .then((responseData) => {
      console.log(responseData);
      newElement = {
        "All Resumes": Object.values(responseData).reduce(
          (acc, curr) => acc + curr,
          0
        ),
      };
      responseData = { ...newElement, ...responseData };
      Folders.MainCategory = Object.keys(responseData);
      toDisplayFloder(responseData);
    });
};

togetFolders();

// Close SubContainer

CloseSubContainer.onclick = () => {
  SubCategorySection.style.display = "none";
  SubCategorySearchFilters.value = "";
  document.getElementById("Dashboard").style.overflow = "auto";
  FilteringData.onFolderSelect = "";
};

window.onload = () => {
  isLogout();
};

function setIds() {
  SearchFilters = document.getElementById("SearchFilters");
  // SearchInput = document.getElementById("SearchInput");
  SearchItems = document.getElementById("SearchItems");
  SearchButton = document.getElementById("SearchButton");
  // ExperienceList = document.getElementById("ExperienceList");
  LocationSuggestions = document.getElementById("LocationSuggestions");
  SuggestionContainer = document.getElementById("SuggestionContainer");
  // ExperienceHeader = document.getElementById("Experience-Header");

  // listItems = document.getElementById("listItems");
  // ExperienceHeader.style.display = "none";

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
  //   }
  // });

  // SearchFilters.addEventListener("text", HoverSuggestionListContainer);
}

document.addEventListener("DOMContentLoaded", async () => {
  // await getHtml();
  setIds();
});

//  settingSuggestionData
tosetSuggestionData = (data) => {
  for (let i of data.SkillList) {
    let li = document.createElement("li");

    li.textContent = i;
    li.id = i;
    li.setAttribute("onclick", () => {
      console.log(this.id);
    });
    SkillSuggestions.appendChild(li);
  }
};

// Clear Sub Folder Search Value

ClearSubFolderSearchValue.addEventListener("click", function () {
  SubCategorySearchFilters.value = "";
  toDisplaySubCategory(Folders.SubCategory);
  ClearSubFolderSearchValue.style.display = "none";
});

//  Search Functionality of Folders

SubCategorySearchFilters.addEventListener("input", function (event) {
  if (event.target.value !== "") {
    ClearSubFolderSearchValue.style.display = "block";
  } else {
    ClearSubFolderSearchValue.style.display = "none";
  }
  Data = {};
  for (let i of Object.keys(Folders.SubCategory)) {
    if (i.toLowerCase().includes(event.target.value.toLowerCase())) {
      Data[i] = Folders.SubCategory[i];
    }
  }
  // Data = Folders.SubCategory.filter((item) =>
  //   item.toLowerCase().includes(event.target.value.toLowerCase())
  // );
  toDisplaySubCategory(Data);
});

// to create SubFolder
document.getElementById("SubFolderAddFolder").onclick = function () {
  document.getElementById("CreateFolders-SubFolders").style.display = "flex";
  SubCategorySection.style.display = "none";
  AddFolderDisplayId.style.display = "block";
  EditFolderDisplayId.style.display = "none";
};

document.getElementById("CategoryAddFolder").onclick = function () {
  document.getElementById("CreateFolders-SubFolders").style.display = "flex";
  AddFolderDisplayId.style.display = "block";
  EditFolderDisplayId.style.display = "none";
};

//  close icon
document.getElementById("CloseAddFolder").onclick = function () {
  document.getElementById("CreateFolders-SubFolders").style.display = "none";
  FilteringData.onFolderSelect = "";
  AddFolderName.value = "";
  AddFolderSkills.value = "";
};

async function addFolder(folderData) {
  const response = await fetch("http://localhost:8000/add_folder/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(folderData),
  });
  if (response.ok) {
    const data = await response.json();
    if (data["status"] === 409) {
      alert("Folder already exists");
    }

    console.log("Folder added successfully:", data);
  } else {
    console.error("Failed to add folder:", response.statusText);
  }
}
document.getElementById("SubmitAddFloder").onclick = function () {
  if (AddFolderName.value.length > 0 && AddFolderSkills.value.length > 0) {
    const folderData = {
      Name: AddFolderName.value,
      Skills: AddFolderSkills.value,
      ParentFolder: FilteringData.onFolderSelect,
    };

    addFolder(folderData);
    AddFolderName.value = "";
    AddFolderSkills.value = "";
    FilteringData.onFolderSelect = "";
    document.getElementById("CreateFolders-SubFolders").style.display = "none";
    FilteringData.page = "main";
    setTimeout(triggerDOMContentLoaded, 400);
    //  triggerDOMContentLoaded();
    togetFolders();
  } else {
    alert("Please fill all the fields to crete Folder");
  }
};

// UploadResumes

UploadResumes.addEventListener("click", () => {
  dialog.showModal();
});

// Update Flag

async function getFlag() {
  const response = await fetch(
    "http://localhost:8000/updateNewDataFlag/",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ folder: FilteringData.onSelectSubFolder }),
    }
  );
  if (response.ok) {
    const data = await response.json();
    console.log(data);
  } else {
    console.error("Failed to get flag:", response.statusText);
  }
}

//  Edit Category
async function EditFolderNamefunction(data) {
  const response = await fetch("http://localhost:8000/editFolderName", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  if (response.ok) {
    const data = await response.json();
    if (data.status === 401) {
      alert(data.action);
    } else {
      alert(data.action);
    }
  } else {
    console.error("Failed to Change:", response.statusText);
  }
}

function EditCategory(data) {
  SubCategorySection.style.display = "none";
  document.getElementById("CreateFolders-SubFolders").style.display = "flex";
  // SubCategorySection.style.display = "none";
  AddFolderDisplayId.style.display = "none";
  EditFolderDisplayId.style.display = "block";
  PreviousFolderName.value = data;
}

document
  .getElementById("SubmitEditFloder")
  .addEventListener("click", function () {
    if (EditFolderName.value.length > 0) {
      const folderData = {
        PrevFolderName: PreviousFolderName.value,
        NewFolderName: EditFolderName.value,
        ParentFolder: FilteringData.onFolderSelect,
      };

      EditFolderNamefunction(folderData);
      EditFolderName.value = "";
      FilteringData.onFolderSelect = "";
      document.getElementById("CreateFolders-SubFolders").style.display =
        "none";
      FilteringData.page = "main";
      setTimeout(triggerDOMContentLoaded, 400);
      // triggerDOMContentLoaded();
      togetFolders();
      EditFolderDisplayId.style.display = "none";
    } else {
      alert("Please fill all the fields to crete Folder");
    }
  });

document.getElementById("CloseEditFolder").onclick = () => {
  document.getElementById("CreateFolders-SubFolders").style.display = "none";
  AddFolderDisplayId.style.display = "none";
  EditFolderDisplayId.style.display = "none";
  FilteringData.onFolderSelect = "";
  AddFolderName.value = "";
  AddFolderSkills.value = "";
};
