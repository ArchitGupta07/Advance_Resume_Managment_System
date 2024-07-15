let resume_filters = {
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
};
// let resume_filters2 = {
//   Candidate: {
//     check: [],

//   },
// };

check_filter = { name: "archit" };

fetch("http://localhost:8000/filter", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify(resume_filters),
})
  .then((response) => response.json())
  .then((data) => {
    console.log(data);
  })
  .catch((error) => {
    console.error("Error:", error);
  });

resume_filters["Education"]["degreee"] = [];
