(function () {
    notificationLength = 0;
    numberOfNotifications = 10;
    loadingMoreNotifications = false;
    toggleDuplicateSelectionVal = false;
    toggleNotifcationListDiv = false;
    latestNotificationDate = undefined;
    notificationInterval = undefined;

})();

// var toggleDuplicateSelectionVal = false;

async function getNotifications(limit) {
    console.log("limit is ", limit);
    try {
        const response = await fetch(
            "http://localhost:8000/get-notifications",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ Limit: limit }),
            }
        );
        const data = await response.json();

        console.log(data);

        return data;
    } catch (error) {
        console.log("failed to fetch notifications: ", error);
    }
}

async function getNotificationDate() {
    try {
        const response = await fetch(
            "http://localhost:8000/get-notification-date",
            {
                method: "POST",
            }
        );
        const data = await response.json();

        console.log("notification date:", data);

        return data;
    } catch (error) {
        console.log("failed to fetch notifications: ", error);
        return '2024-06-13T06:38:33.644608'
    }
}

notificationInterval = setInterval(async () => {
    const notificationDate = await getNotificationDate();
    console.log(notificationDate)
    const newDate = new Date(notificationDate);
    if (!latestNotificationDate || !newDate) {
        if (!notificationDate) {
            notificationDate = '2024-06-13T06:38:33.644608'
        }
        latestNotificationDate = notificationDate;
        console.log('latestNotificationDate not defined')
        // clearInterval(notificationInterval);
    } else {
        const oldDate = new Date(latestNotificationDate);
        if (newDate > oldDate) {
            console.log("dot set");
            document.getElementById("notification-dot").style.display = "block";
            // await notificationsInIt()
        }
        latestNotificationDate = notificationDate;
    }
}, 5000);

function onClickOpenErrorModal(event) {
    const dataValues = event.target.getAttribute("data-values");
    const dataValuesFinal = JSON.parse(dataValues);
    console.log(dataValuesFinal);
    console.log(
        "onclick ",
        dataValuesFinal["data"],
        dataValuesFinal["statusId"],
        dataValuesFinal["filecount"]
    );
    viewUploadErrorDetails(
        dataValuesFinal["data"],
        dataValuesFinal["statusId"],
        dataValuesFinal["filecount"]
    );
}

formatDateTimeString = (utcDateString) => {
    if (!utcDateString) return "";

    const utcDate = new Date(utcDateString);

    // Convert UTC time to IST by adding 5 hours and 30 minutes (19800000 milliseconds)
    const istOffsetMilliseconds = 5.5 * 60 * 60 * 1000;
    const istDate = new Date(utcDate.getTime() + istOffsetMilliseconds);

    const month = istDate.getMonth() + 1; // getMonth() is zero-based
    const year = istDate.getFullYear();
    const day = istDate.getDate();

    const hours = istDate.getHours();
    const minutes = istDate.getMinutes();
    const seconds = istDate.getSeconds();

    const monthNames = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ];
    const monthName = monthNames[month - 1];

    const formattedDate = `${monthName} ${day}, ${year}`;
    const formattedTime = `${String(hours).padStart(2, "0")}:${String(
        minutes
    ).padStart(2, "0")}:${String(seconds).padStart(2, "0")} IST`;

    return `${formattedDate} ${formattedTime}`;
};

async function notificationsInIt() {
    document.getElementById("notification-dot").style.display = "none";
    toggleNotifcationListDiv = true;
    document.getElementById("notification-container").style.height = "60vh";
    data = await getNotifications(numberOfNotifications);
    notificationLength = data.length;

    const notificationList = document.getElementById("notifications-list");

    if (notificationLength == 0) {
        document.getElementById('no-noti-message').style.display = 'block'
        // document.getElementById('noti-loader-div').style.display = 'none';
        notificationList.innerHTML = "";
        document.getElementById('clear-all').style.display = 'none';
        return;
    }

    document.getElementById('clear-all').style.display = 'block';
    latestNotificationDate = data[0][4];

    console.log("data length:", data);


    notificationList.innerHTML = "";

    for (i of data) {
        console.log("error for notification: ", i, " ", i[6]);
        const status = i[6].status;

        const tempJson = i[2];
        const formattedDate = formatDateTimeString(i[4]);
        console.log(i[2]);
        const notificationJson = JSON.parse(tempJson);

        const fileCount = notificationJson.fileCount;

        const notificationDiv = document.createElement("div");
        notificationDiv.classList.add("sec");

        const txtDiv = document.createElement("div");
        txtDiv.classList.add("txt");
        txtDiv.textContent = `A new upload session of ${fileCount} file${fileCount == 1 ? "" : "s"
            } was created!`;

        notificationDiv.appendChild(txtDiv);

        const subDiv = document.createElement("div");
        subDiv.classList.add("txt", "sub", "flex-span");

        const dateSpan = document.createElement("span");
        dateSpan.textContent = formattedDate;

        const statusSpan = document.createElement("span");
        statusSpan.id = i[0];
        statusSpan.setAttribute(
            "data-values",
            JSON.stringify({ data: i[6], statusId: i[0], filecount: fileCount })
        );

        console.log("this is???", i[6]);

        if (status == "error") {
            statusSpan.classList.add("errorSpan");

            statusSpan.addEventListener("click", onClickOpenErrorModal);
            statusSpan.textContent = "Error";
        } else if (status == "inProgress") {
            statusSpan.classList.add("inProgressSpan");
            statusSpan.textContent = "InProgress";
        } else if (status == "success") {
            statusSpan.classList.add("successSpan");
            statusSpan.textContent = "Success";
        }
        // statusSpan.addEventListener('click', () => {
        //   viewUploadErrorDetails();
        // })

        subDiv.appendChild(dateSpan);
        subDiv.appendChild(statusSpan);

        notificationDiv.appendChild(subDiv);

        notificationList.appendChild(notificationDiv);
    }

    const loadMoreNotifications = document.createElement("div");
    loadMoreNotifications.id = 'loadmorenotificationsdiv'
    loadMoreNotifications.classList.add("loadMoreNotifications");
    const loadMoreSpan = document.createElement("span");
    loadMoreSpan.id = "loadmorenotifications";
    loadMoreSpan.classList.add("loadMoreNotificationsText");
    loadMoreSpan.textContent = "Load More Notifications";
    loadMoreNotifications.appendChild(loadMoreSpan);
    if (notificationLength >= 10) {
        notificationList.appendChild(loadMoreNotifications);
    }

    loadMoreSpan.addEventListener("click", () => {
        console.log("load more was clicked");
        numberOfNotifications = numberOfNotifications + 10;
        document.getElementById("loadmorenotifications").style.display = "none";
        document.getElementById("load-more-loader").style.display = "block";
        notificationsInIt();
    });

    const loadMoreSpinner = document.createElement("div");
    loadMoreSpinner.id = "load-more-loader";
    loadMoreSpinner.classList.add("load-more-spinner");
    loadMoreSpinner.style.display = "none";
    loadMoreNotifications.append(loadMoreSpinner);
}

window.addEventListener("click", async function (event) {
    const notificationContainer = document.getElementById(
        "notification-container"
    );
    const icon = document.getElementById("icon");
    const uploadErrorDialog = document.getElementById("uploadDialog");

    const singleResumeViewer = document.getElementById("viewResumesection");
    const multipleResumeViewer = document.getElementById("compareViewResume");

    // console.log('single viewer ', singleResumeViewer)
    // console.log('multiple viewer ', multipleResumeViewer)

    console.log('toggleNotifcationListDiv is: ', toggleNotifcationListDiv)

    if (
        !notificationContainer.contains(event.target) &&
        !icon.contains(event.target) &&
        !uploadErrorDialog.contains(event.target) &&
        !singleResumeViewer.contains(event.target) &&
        !multipleResumeViewer.contains(event.target)
    ) {
        notificationContainer.style.height = "0";
        toggleNotifcationListDiv = false;
    }

    if (icon.contains(event.target) && toggleNotifcationListDiv == true) {
        console.log('toggleNotifcationListDiv inside the condition is: ', toggleNotifcationListDiv)
        toggleNotifcationListDiv = false;
        notificationContainer.style.height = "0";
    }

    else if (icon.contains(event.target) && toggleNotifcationListDiv == false) {
        console.log('toggleNotifcationListDiv inside the condition is: ', toggleNotifcationListDiv)
        toggleNotifcationListDiv = true;
        await notificationsInIt();
    }
});

function loadNotifications() {
    if (toggleNotifcationListDiv != true) {
        toggleNotifcationListDiv = true;
        notificationsInIt();
    }

}

// document.getElementById("icon").addEventListener("click", () => {
//   //mark all notifications as seen
// })

// const formatDateTimeString = (utcDateString) => {
//   if (!utcDateString) return ''

//   const utcDate = new Date(utcDateString)

//   // Create a new Date object representing the UTC date and time
//   const utcOffsetMinutes = utcDate.getTimezoneOffset()
//   const istOffsetMinutes = utcOffsetMinutes + 330 // IST is UTC + 5:30 which is 330 minutes

//   const istDate = new Date(utcDate.getTime() + istOffsetMinutes * 60 * 1000)

//   const month = istDate.getMonth() + 1 // getMonth() is zero-based
//   const year = istDate.getFullYear()
//   const day = istDate.getDate()

//   const hours = istDate.getHours()
//   const minutes = istDate.getMinutes()
//   const seconds = istDate.getSeconds()

//   const monthNames = [
//     'January',
//     'February',
//     'March',
//     'April',
//     'May',
//     'June',
//     'July',
//     'August',
//     'September',
//     'October',
//     'November',
//     'December'
//   ]
//   const monthName = monthNames[month - 1]

//   const formattedDate = `${monthName} ${day}, ${year}`
//   const formattedTime = `${String(hours).padStart(2, '0')}:${String(
//     minutes
//   ).padStart(2, '0')}:${String(seconds).padStart(2, '0')} IST`

//   return `${formattedDate} ${formattedTime}`
// }

// Example usage
// console.log(formatDateTimeString("2024-05-21T12:00:00Z") // Outputs: May 21, 2024 17:30:00 IST

function viewUploadErrorDetails(errors, statusId, filecount) {
    let countCorruptRecords = 0;
    let countDuplicateRecords = 0;

    document.getElementById("duplicate-records").textContent = "";
    document.getElementById("corrupt-records").textContent = "";
    document.getElementById("duplicate-loader").style.display = "block";
    // errors = JSON.parse(errorDetailsObj)
    console.log("these are error details: ", errors.errors);

    for (error of errors.errors) {
        files = error.split(",");
        console.log("error: ", error);
        console.log("these are files: ", files);
        if (files.length < 3) {
            countCorruptRecords++;
            createCorruptRecord(error);
            console.log("file length less than 3??");
            continue;
        }

        countDuplicateRecords++;
        createDuplicateRecord(files[0], files[1], files[2], statusId, filecount);
    }

    if (countDuplicateRecords == 0) {
        document.getElementById("duplicate-wrapper").style.display = "none";
        document.getElementById("duplicate-loader").style.display = "none";
        document.getElementById("duplicate-records").textContent =
            "No Records To Show";
    }

    if (countCorruptRecords == 0) {
        document.getElementById("corrupt-wrapper").style.display = "none";
        document.getElementById("corrupt-records").textContent =
            "No Records To Show";
    }

    document.getElementById("showerrordialog").style.display = "flex";
}

document.getElementById("closeerror-btn").addEventListener("click", () => {
    document.getElementById("showerrordialog").style.display = "none";
});

function createCorruptRecord(error) {
    document.getElementById("corrupt-wrapper").style.display = "block";
    console.log("\n Corrupt record error", error, " \n");
    filename = error.split("!@&")[1];

    // <div class="duplicate-record-file-div">Hello world</div>

    let duplicateFileDiv = document.createElement("div");
    duplicateFileDiv.className = "duplicate-record-file-div";
    duplicateFileDiv.textContent = filename;

    document.getElementById("corrupt-records").appendChild(duplicateFileDiv);
}

async function createDuplicateRecord(file1, file2, logId, statusId, filecount) {
    document.getElementById("duplicate-wrapper").style.display = "block";
    // filename1 = file1;
    // filename2 = file2;

    // fetch('getLinkAndDateFromFileName', { method: 'POST', body: { 'file1': `${filename1}`, 'file2': `${filename2}` } })
    let filename1 = file1.split("!@&")[1];
    let filename2 = file2.split("!@&")[1];
    let filename1Display = filename1.slice(0, 18);
    let filename2Display = filename2.slice(0, 18);
    filename1Display += "...";
    filename2Display += "...";

    let data;
    try {
        const response = await fetch(
            "http://localhost:8000/getLinkAndDateFromFileName",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ file1: file1, file2: file2 }),
            }
        );

        if (!response.ok) {
            throw new Error("Network response was not ok");
        }

        data = await response.json();
    } catch (error) {
        console.log(error);
    }

    filelink1 = data.filelink1;
    filelink2 = data.filelink2;
    datetime1 = formatDateTimeString(data.filetime1);
    datetime2 = formatDateTimeString(data.filetime2);

    console.log("response from error api****", data);

    // Create main container div

    const duplicateRecord = document.createElement("div");
    duplicateRecord.className = "duplicate-record";
    duplicateRecord.id = logId;

    // Create checkbox
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.style.width = "1.5rem";
    checkbox.style.height = "1.5rem";
    checkbox.style.background = "blue";
    checkbox.autocomplete = "off";
    checkbox.name = "checkbox";
    checkbox.setAttribute(
        "data-values",
        JSON.stringify({
            data: `${file1},${file2},${logId}`,
            statusId: statusId,
            filecount: filecount,
            logId: logId,
        })
    );

    duplicateRecord.appendChild(checkbox);

    // Create grid container
    const bothFilesGrid = document.createElement("div");
    bothFilesGrid.className = "both-files-grid";
    duplicateRecord.appendChild(bothFilesGrid);

    // Create first file div
    const fileDiv1 = document.createElement("div");
    fileDiv1.className = "duplicate-record-file-div";
    bothFilesGrid.appendChild(fileDiv1);

    // Create first file details
    const fileDetails1 = document.createElement("div");
    fileDetails1.className = "duplicate-record-file-details";
    fileDiv1.appendChild(fileDetails1);

    const fileName1 = document.createElement("span");
    fileName1.className = "duplicate-record-file-details-name";
    fileName1.textContent = filename1Display;
    fileDetails1.appendChild(fileName1);

    const fileDateTime1 = document.createElement("span");
    fileDateTime1.className = "duplicate-record-file-details-datetime";
    fileDateTime1.textContent = datetime1;
    fileDetails1.appendChild(fileDateTime1);

    // Create first file action
    const flex1 = document.createElement("div");
    flex1.className = "flex items-center";
    fileDiv1.appendChild(flex1);

    const svg1 = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg1.classList.add("duplicate-action");
    const use1 = document.createElementNS("http://www.w3.org/2000/svg", "use");
    use1.setAttributeNS(
        "http://www.w3.org/1999/xlink",
        "xlink:href",
        "./Icons/icons.svg#ActionIcon"
    );
    svg1.appendChild(use1);
    flex1.appendChild(svg1);

    svg1.setAttribute("data-values", JSON.stringify(filelink1));
    svg1.style.cursor = "pointer";

    svg1.addEventListener("click", (event) => {
        const dataValues = event.target.getAttribute("data-values");
        const dataValueslink = JSON.parse(dataValues);
        openSingleFileViewer(dataValueslink);
    });

    // Create second file div
    const fileDiv2 = document.createElement("div");
    fileDiv2.className = "duplicate-record-file-div";
    bothFilesGrid.appendChild(fileDiv2);

    // Create second file details
    const fileDetails2 = document.createElement("div");
    fileDetails2.className = "duplicate-record-file-details";
    fileDiv2.appendChild(fileDetails2);

    const fileName2 = document.createElement("span");
    fileName2.className = "duplicate-record-file-details-name";
    fileName2.textContent = filename2Display;
    fileDetails2.appendChild(fileName2);

    const fileDateTime2 = document.createElement("span");
    fileDateTime2.className = "duplicate-record-file-details-datetime";
    fileDateTime2.textContent = datetime2;
    fileDetails2.appendChild(fileDateTime2);

    // Create second file actions
    const secondActions = document.createElement("div");
    secondActions.className = "second-duplicate-cta-actions";
    fileDiv2.appendChild(secondActions);

    const flex2 = document.createElement("div");
    flex2.className = "flex items-center";
    secondActions.appendChild(flex2);

    const svg2 = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg2.classList.add("duplicate-action");
    const use2 = document.createElementNS("http://www.w3.org/2000/svg", "use");
    use2.setAttributeNS(
        "http://www.w3.org/1999/xlink",
        "xlink:href",
        "./Icons/icons.svg#ActionIcon"
    );
    svg2.appendChild(use2);
    flex2.appendChild(svg2);

    svg2.setAttribute("data-values", JSON.stringify(filelink2));
    svg2.style.cursor = "pointer";

    svg2.addEventListener("click", (event) => {
        const dataValues = event.target.getAttribute("data-values");
        const dataValueslink = JSON.parse(dataValues);
        openSingleFileViewer(dataValueslink);
    });

    const compareSpan = document.createElement("span");
    compareSpan.style.color = "blue";
    compareSpan.style.textDecoration = "underline";
    compareSpan.textContent = "Compare";
    secondActions.appendChild(compareSpan);

    compareSpan.style.cursor = "pointer";

    compareSpan.setAttribute(
        "data-values",
        JSON.stringify(`${filelink1}]!@&[${filelink2}`)
    );

    compareSpan.addEventListener("click", (event) => {
        const dataValues = event.target.getAttribute("data-values");
        const dataValueslink = JSON.parse(dataValues);

        firstDataValueLink = dataValueslink.split("]!@&[")[0];
        secondDataValueLink = dataValueslink.split("]!@&[")[0];

        console.log(
            "compare button clicked: ",
            firstDataValueLink,
            " ",
            secondDataValueLink
        );
        openResumeComparer(firstDataValueLink, secondDataValueLink);
    });

    // Append the complete structure to the container
    document.getElementById("duplicate-loader").style.display = "none";
    document.getElementById("duplicate-records").appendChild(duplicateRecord);
}

// End of the above function here

document.getElementById("discardBtn").addEventListener("click", (event) => {
    clickedButton = "discard";
});

document.getElementById("replaceBtn").addEventListener("click", (event) => {
    clickedButton = "replace";
});

document
    .getElementById("replaceOrDiscard")
    .addEventListener("submit", async function (event) {
        event.preventDefault();

        document.getElementById("showerrordialog").style.display = "none";

        var selectedCheckboxes = document.querySelectorAll(
            'input[name="checkbox"]:checked'
        );

        const unselectedCheckboxes = document.querySelectorAll(
            'input[name="checkbox"]:not(:checked)'
        );
        var dataValues = [];
        var dataValues2 = [];
        let statusId;
        let filecount;

        selectedCheckboxes.forEach(function (checkbox) {
            const obj = JSON.parse(checkbox.dataset.values);
            statusId = obj["statusId"];
            filecount = obj["filecount"];
            // let node = document.getElementById(obj['logId'])
            // console.log('logid: ', obj['logId'])
            // node.parentNode.removeChild(node)
            // document.getElementById('bothErrorGrid').style.display = 'none';
            // document.getElementById('replaceordiscardLoader').style.display = 'block';
            dataValues.push(obj["data"]);
        });

        let count2 = 0;

        unselectedCheckboxes.forEach(function (checkbox) {
            const obj = JSON.parse(checkbox.dataset.values);
            statusId = obj["statusId"];
            filecount = obj["filecount"];
            dataValues2.push(obj["data"]);
            count2++;
        });

        console.log(
            "data values 2 have count: ",
            count2,
            "and value = ",
            dataValues2
        );

        const statusSpanToRemove = document.getElementById(statusId);

        statusSpanToRemove.textContent = "Success";
        statusSpanToRemove.classList.remove("errorSpan");
        statusSpanToRemove.classList.add("successSpan");
        statusSpanToRemove.removeEventListener("click", onClickOpenErrorModal);

        // if (document.getElementById('duplicate-records').innerHTML === '') {
        //   document.getElementById('duplicate-wrapper').style.display = 'none';
        // }

        console.log(dataValues);

        const updating = await fetch(
            "http://localhost:8000/markNotificationAsResolved",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ NotifID: statusId }),
            }
        );

        if (clickedButton == "replace") {
            const data = await fetch("http://localhost:8000/replace_resume", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(dataValues),
            });
        }

        if (clickedButton == "discard") {
            const data = await fetch("http://localhost:8000/replace_resume", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(dataValues2),
            });
        }

        await notificationsInIt();

        // document.getElementById('bothErrorGrid').style.display = 'block';
        // document.getElementById('replaceordiscardLoader').style.display = 'none';

        // console.log("status id: ", statusId)
        // console.log("fileCount: ", filecount)

        // // await restartModal(statusId, filecount);

        // console.log("resume replaced?", data)

        // console.log(dataValues)

        // console.log("clickedButton", clickedButton)
    });

async function restartModal(statusId, filecount) {
    const data = await fetch("http://localhost:8000/refresh-modal", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            statusId: `${statusId}`,
            filecount: `${filecount}`,
        }),
    });

    const dataval = await data.json();

    console.log("api data: ", dataval);

    console.log("restart Modal status");

    // const dataValues = document.getElementById(statusId).getAttribute("data-values")
    // console.log('data values are: ', dataValues)
    viewUploadErrorDetails(dataval, statusId);
    // document.getElementById('bothErrorGrid').style.display = 'block';
    // document.getElementById('replaceordiscardLoader').style.display = 'none';
}
// createDuplicateRecord();
// createDuplicateRecord();

// fetchviewdata = async (filename) => {
//   let data = "";

//   let url = new URL("http://localhost:8000/view-resume");
//   url.search = new URLSearchParams(idvalue).toString();
//   let response = await fetch(url);
//   data = await response.json();
//   if (data) {
//     viewcandidatedata.src = getFileViewerUrl(data);
//   }
//   viewsection.style.display = "flex";
// };

function getFileViewerUrl(fileUrl) {
    const decodedUrl = decodeURIComponent(fileUrl);
    console.log("decoded url: ", decodedUrl);
    const fileExtension = getFileExtension(decodedUrl);
    console.log("extension after decoding: ", fileExtension);

    switch (fileExtension) {
        case "pdf":
            return fileUrl;
        case "doc":
        case "docx":
            return `https://view.officeapps.live.com/op/embed.aspx?src=${encodeURIComponent(
                fileUrl
            )}`;
        case "jpg":
        case "jpeg":
        case "png":
        case "gif":
            return fileUrl;
        default:
            return fileUrl;
            alert("File type not supported!");
            return "";
    }
}

function getFileExtension(url) {
    const parts = url.split(".");
    console.log("moon", parts);
    if (parts.length > 1) {
        return parts.pop().toLowerCase().split("?")[0];
    }
    return "";
}

function openSingleFileViewer(fileLink) {
    console.log(fileLink);
    console.log("before src: ", fileLink.length);

    document.getElementById("viewresssdata").src = getFileViewerUrl(fileLink);
    console.log("html view resume", document.getElementById("viewresssdata"));
    document.getElementById("viewResumesection").style.display = "flex";
}

document.getElementById("viewdatacloseicon").addEventListener("click", () => {
    document.getElementById("viewResumesection").style.display = "none";
    document.getElementById("viewResumesection").src = "";
});

function openResumeComparer(filelink1, filelink2) {
    document.getElementById("resumeViewOne").src = getFileViewerUrl(filelink1);
    document.getElementById("resumeViewTwo").src = getFileViewerUrl(filelink2);

    document.getElementById("compareViewResume").style.display = "flex";
}

document.getElementById("CompareViewClose").addEventListener("click", () => {
    document.getElementById("resumeViewOne").src = "";
    document.getElementById("resumeViewTwo").src = "";
    document.getElementById("compareViewResume").style.display = "none";
});

// function xyz() {
//     let toggleDuplicateSelectionVal = false


//     document
//         .getElementById("toggleDuplicateSelection")
//         .addEventListener("click", () => {
//             if (toggleDuplicateSelectionVal === false) {
//                 document.getElementById("toggle-select-text").textContent =
//                     "Deselect All";
//                 toggleDuplicateSelectionVal = true;
//                 console.log('hello')
//                 selectAllCheckboxes();
//             } else {
//                 document.getElementById("toggle-select-text").textContent = "Select All";
//                 toggleDuplicateSelectionVal = false;
//                 console.log('hello2')
//                 unselectAllCheckboxes();
//             }
//         });

// }

// xyz();

document.getElementById("toggleDuplicateSelection")
    .addEventListener("click", () => {
        if (toggleDuplicateSelectionVal === false) {
            document.getElementById("toggle-select-text").textContent =
                "Deselect All";
            toggleDuplicateSelectionVal = true;
            console.log('hello')
            selectAllCheckboxes();
        } else {
            document.getElementById("toggle-select-text").textContent = "Select All";
            toggleDuplicateSelectionVal = false;
            console.log('hello2')
            unselectAllCheckboxes();
        }
    });


function selectAllCheckboxes() {
    var checkboxes = document.querySelectorAll(
        '#duplicate-records input[type="checkbox"]'
    );
    checkboxes.forEach(function (checkbox) {
        checkbox.checked = true;
    });
}

function unselectAllCheckboxes() {
    var checkboxes = document.querySelectorAll(
        '#duplicate-records input[type="checkbox"]'
    );
    checkboxes.forEach(function (checkbox) {
        checkbox.checked = false;
    });
}

console.log(document.getElementById('clear-all'))
document.getElementById('clear-all').addEventListener('click', async () => {
    document.getElementById("notifications-list").innerHTML = ''
    document.getElementById('clear-all').style.display = 'none';
    console.log('hello')
    const response = await fetch('http://localhost:8000/clear-all-notifications', {
        method: 'POST'
    })

    notificationsInIt();

    console.log('clear all called: ', response)

})
