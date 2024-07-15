// document.addEventListener('DOMContentLoaded', function () {
//     document.getElementById('upload-btn').addEventListener('click', function (event) {
//         event.preventDefault();
//         console.log('Upload button clicked, about to call upload function.');
//         upload();

//     });
// });

document
  .getElementById("upload-btn")
  .addEventListener("click", function (event) {
    event.preventDefault();
    console.log("Upload button clicked, about to call upload function.");
    upload();
  });

const maxFileSize = 2000 * 1024 * 1024; //2MB
let fileList;
const progressBarOverall = document.getElementById("progressBarOverall");
let uploadedCount;

let uploadingQueue = new Map();
let successfulUploadQueue = new Map();
let failedUploadQueue = new Map();

let fileProgressList = new Map();

let fileObjProgressMapping = new Map();

let ProgressCancelMapping = new Map();
let cancelQueue = new Map();

let cancelledFlag = 0;

function waitForCondition(i) {
  return new Promise((resolve) => {
    const interval = setInterval(() => {
      if (uploadingQueue.size < 5) {
        clearInterval(interval);
        resolve();
      }
    }, 100); // Check every 1/10 th second, adjust the interval as needed
  });
}

//condition will become uploadingQueue size less than 5

const upload = async () => {
  document.getElementById("upload-btn").disabled = true;

  fileList = document.getElementById("fileInput").files;
  // document.getElementById('fileInput').value = ''

  progressBarOverall.max = fileList.length;

  for (let i = 0; i < fileList.length; i++) {
    const file = fileList[i];
    const fileID = file.name + file.type + i;
    const fileProgress = createProgress(file.name, fileID);
    fileProgressList.set(fileID, fileProgress);
    document.getElementById("queue-list").appendChild(fileProgress);
  }

  uploadedCount = 0;

  for (let i = 0; i < fileList.length; i++) {
    await waitForCondition(i); // checks if files are uploaded every 5 files

    const file = fileList[i];

    const fileHash = await calculateHash(file);

    // Database query to check if file exists in db already
    //If so continue and dont proceed further

    console.log(fileHash);

    if (file.size > maxFileSize) {
      alert("File Uploaded exceeds limit", file.name);
      continue;
    }

    const fileID = file.name + file.type + i;

    const fileObj = {
      fileName: file.name,
      fileid: fileID,
      file: file,
      updatedAt: Date.now(),
    };

    uploadingQueue.set(fileID, fileObj);

    console.log(file.name); // Print the name of each selected file

    const formData = new FormData();
    formData.append("file", file);

    const fileProgress = fileProgressList.get(fileID); // Create progress bar for the file

    fileObjProgressMapping.set(fileProgress, fileObj);

    if (cancelQueue.get(fileProgress) == 1) continue; // maybe I should make a good file metadata json or something with status, it will make this easy to work with

    updateProgress(fileProgress, 0);

    listAppend(1, fileProgress);

    try {
      const response = uploadDoc(fileID, formData, fileProgress);
    } catch (error) {
      console.error(`Failed to upload file ${file.name}: ${error}`);
    }
  }

  document.getElementById("upload-btn").disabled = false;
};

const uploadDoc = async (fileID, formData, fileProgress) => {
  const cancelToken = new axios.CancelToken((cancel) => {
    const fileCancel = cancel;
    ProgressCancelMapping.set(fileID, cancel);
    //  console.log("cancel ",fileCancel)
  });

  try {
    const response = await axios.post(
      "http://localhost:8000/items/",
      formData,
      {
        cancelToken,
        onUploadProgress: (progressEvent) => {
          const progress = Math.round(
            (progressEvent.loaded / progressEvent.total) * 100
          );
          updateProgressBar(progress);
        },
      }
    );

    if (response.status !== 200) {
      throw new Error("Failed to upload file");
    }

    uploadedCount++;
    successfulUploadQueue.set(fileID, uploadingQueue.get(fileID));
    listAppend(2, fileProgress);
    uploadingQueue.delete(fileID);
    updateOverallProgressBar(
      progressBarOverall,
      uploadedCount,
      fileList.length
    );
    updateProgress(fileProgress, 1); //change image
    console.log(`File ${formData.get("file").name} uploaded successfully`);

    return response.data;
  } catch (error) {
    updateProgress(fileProgress, 2); //change image

    if (cancelledFlag === 1) {
      cancelledFlag = 0;
    } else {
      failedUploadQueue.set(fileID, uploadingQueue.get(fileID));
      uploadingQueue.delete(fileID);

      listAppend(3, fileProgress);
    }
    throw error;
  }
};

const updateProgressBar = (progress) => {
  document.getElementById("progress-bar").value = progress;
  document.getElementById(
    "individual-progress"
  ).innerHTML = `Upload Progress: ${progress}%`;
};

const updateProgress = (fileProgress, imgVal) => {
  if (imgVal == 0) {
    fileProgress.children[1].src =
      "https://res.cloudinary.com/dfoa0w717/image/upload/v1711519204/Spinner-1s-200px_acyihi.gif";
  }
  if (imgVal === 1) {
    fileProgress.children[1].src =
      "https://res.cloudinary.com/dfoa0w717/image/upload/v1711519204/Tick_twl0em.png";
  } else if (imgVal === 2) {
    fileProgress.children[1].src =
      "https://res.cloudinary.com/dfoa0w717/image/upload/v1711519204/cross_ytrr8v.png";
  }
};

const updateOverallProgressBar = (progressBar, count, total) => {
  document.getElementById("progressNumbers").innerHTML = `${count}/${total}`;
  progressBar.value = count;
};

const createProgress = (fileName, fileID) => {
  const container = document.createElement("div");
  container.setAttribute("id", fileID);
  container.classList.add("file-upload-item");

  const label = document.createElement("span");
  label.textContent = fileName;
  container.appendChild(label);

  const loader = document.createElement("img");

  loader.src =
    "https://res.cloudinary.com/dfoa0w717/image/upload/v1711617751/noun-pending-folder-6269561_1_dm1deg.png";
  loader.classList.add("file-progress");
  // progressBar.value = 0;
  // progressBar.max = 100;
  loader.setAttribute("id", "progress-image");
  container.appendChild(loader);

  const cancelButton = document.createElement("button");
  // cancelButton.setAttribute('id','cancel-button')
  cancelButton.innerHTML = "Cancel";
  cancelButton.setAttribute("onclick", `cancelUpload(this)`);
  container.appendChild(cancelButton);

  return container;
};

const listAppend = (type, fileProgress) => {
  if (type == 1) {
    document.getElementById("upload-list").appendChild(fileProgress);
  } else if (type == 2) {
    document.getElementById("success-list").appendChild(fileProgress);
    // const cancelBtn = document.getElementById('cancel-button')
    fileProgress.removeChild(fileProgress.children[2]);
  } else if (type == 3) {
    document.getElementById("failed-list").appendChild(fileProgress);
    // const cancelBtn = document.getElementById('cancel-button')
    fileProgress.removeChild(fileProgress.children[2]);

    const retryButton = document.createElement("button");
    // cancelButton.setAttribute('id','cancel-button')
    retryButton.innerHTML = "Retry";
    retryButton.setAttribute("onclick", `retryUpload(this)`);
    fileProgress.appendChild(retryButton);
  }
};

const listRemove = (type, fileProgress, fileID) => {
  if (type == 1) {
    document.getElementById("upload-list").removeChild(fileID);
  } else if (type == 2) {
    document.getElementById("success-list").removeChild(fileID);
  } else if (type == 3) {
    document.getElementById("failed-list").removeChild(fileID);
  }
};

const cancelUpload = (container) => {
  cancelledFlag = 1;
  const progress = container.parentNode;
  cancelQueue.set(progress, 1);
  cancelReq = ProgressCancelMapping.get(progress.id);
  document.getElementById("cancelled-list").appendChild(progress);
  progress.removeChild(progress.children[2]);
  cancelReq();
};

const retryUpload = (container) => {
  const progress = container.parentNode;
  const fileObj = fileObjProgressMapping.get(progress);
  console.log(fileObj);

  const formData = new FormData();
  formData.append("file", fileObj.file);

  listAppend(1, progress);

  uploadDoc(fileObj.fileid, formData, progress);
};

function calculateHash(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = (event) => {
      const arrayBuffer = event.target.result;
      const hash = sha256(new Uint8Array(arrayBuffer));
      resolve(hash);
    };
    reader.onerror = (error) => {
      reject(error);
    };
    reader.readAsArrayBuffer(file);
  });
}

function sha256(arrayBuffer) {
  const wordArray = CryptoJS.lib.WordArray.create(arrayBuffer);
  return CryptoJS.SHA256(wordArray).toString(CryptoJS.enc.Hex);
}
