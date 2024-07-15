let FilteringData = {
  FetchedData: [],
  LocationCities: [],
  Skills: [],
  AllSkills: [],
  onSelectSubFolder: "",
  onFolderSelect: "",
  onFolderValue: true,
  page: "",
  chatbotResumeIds: [],
  chatbotData: false,
  QueryonProcess: false,
  dataparaelement: "",
  TemporaryData: [],


};


// let toggleDuplicateSelectionVal = false;



let loaded = false;

window.onload = () => {
  isLogout();
};
document.addEventListener("DOMContentLoaded", async () => {
  if (sessionStorage.getItem("data")) {
    FilteringData = JSON.parse(sessionStorage.getItem("data"));
    console.log(FilteringData);
    sessionStorage.removeItem("data");
    // FilteringData.onFolderSelect = "";
    await getHtml();
  }
  if (FilteringData.page === "") {
    // FilteringData.page = "main";
    await getHtml();
    await getMainHtml(true);
    // tomodal();
  } else if (FilteringData.page === "main") {
    // FilteringData.page = "data";
    await getMainHtml(false);
  } else {
    // FilteringData.page = "main";
    await getContentHtml();
  }
});

async function triggerDOMContentLoaded() {
  const DOMContentLoadedEvent = new Event("DOMContentLoaded");
  console.log(FilteringData.page);
  document.dispatchEvent(DOMContentLoadedEvent);
}

// refresh
window.addEventListener("beforeunload", function (event) {
  if (FilteringData.page === "data") {
    let data = FilteringData;
    data = JSON.stringify(data);
    this.sessionStorage.setItem("data", data);
    // return "Are you sure you want to leave this page?";
  }
});
// window.onbeforeunload = null;

// BackLoad

window.addEventListener("popstate", (event) => {
  console.log(FilteringData.page);
  if (FilteringData.page === "data") {
    FilteringData.page = "main";
    triggerDOMContentLoaded();
  }
  return true;
});

const Filterdata = {
  Candidate: {
    check: [],
    FirstName: [],
    LastName: [],
    Experience: [],
    UploadDate: [],
  },

  WorkExperience: {
    check: [],
    Location: [],
  },

  Education: {
    check: [],
    Degree: [],
    Score: [],
    YearOfPassing: [],
    Branch: [],
    Institution: [],
  },
  Contact: {
    check: [],
    Contact_type: [],
    Contact_value: [],
  },
  Skill: {
    check: [],
    // SkillName: ["Java", "Python"],
    SkillName: [],
  },
  ResumeIdList: {
    check: [],
    ResumeIdValue: [],
  },
};

window.triggerDOMContentLoaded = triggerDOMContentLoaded;
