const UploadWrapperChild = document.getElementById(
  "upload-child-wrapper"
).innerHTML
function fileuplodInit() {
  document.getElementById("fileInput").disabled = false
  const uploadDiv = document.getElementById("upload-zone")
  const fileInput = document.getElementById("fileInput")
  const drivelink = document.getElementById("drivelink")
  const filesList = document.getElementById("fileList")
  const uploadResetBtn = document.getElementById("upload-reset")
  const uploadMoreFiles = document.getElementById("upload-more-files")

  uploadResetBtn.addEventListener("click", function (event) {
    currentUploadCancelled = true
    uploadReset()
    document.getElementById("continue-upload").style.display = "none"
    document.getElementById("dialog").close()
  })

  uploadMoreFiles.addEventListener("click", function (event) {
    uploadReset()
    uploadMoreFiles.style.display = "none"
  })

  uploadDiv.addEventListener("click", function (event) {
    if (event.target !== drivelink) {
      // If not, trigger the file input click event
      fileInput.click()
    }
  })

  // Add drag-and-drop event listeners to the div
  uploadDiv.addEventListener("dragover", function (event) {
    // Prevent default behavior to allow dropping
    event.preventDefault()
    uploadDiv.classList.add("dragging")
  })

  uploadDiv.addEventListener("dragleave", function () {
    // Remove dragging style when drag leaves the div
    uploadDiv.classList.remove("dragging")
  })

  uploadDiv.addEventListener("drop", function (event) {
    // Prevent default behavior and stop event propagation
    event.preventDefault()
    uploadDiv.classList.remove("dragging")

    // Access the dropped files
    const files = event.dataTransfer.files

    // Set the dropped files in the file input element
    fileInput.files = files

    document.getElementById("FileRefCount").innerHTML = fileInput.files.length
    document.getElementById("FileRefCount-div").style.display = "block"

    // Optional: Handle the file selection
    if (files.length > 0) {
      console.log("Dropped files:", files)
      // Perform desired action with the files (e.g., uploading)
    }
  })

  fileInput.addEventListener("change", function () {
    document.getElementById("upload-btn").disabled = false
    document.getElementById("upload-btn").style.display = "block"
    document.getElementById("upload-click-div").style.display = "none"

    const files = fileInput.files
    // console.log('files length', files.length)
    document.getElementById("FileRefCount").innerHTML = files.length
    document.getElementById("FileRefCount-div").style.display = "block"

    // Clear previous list
    filesList.innerHTML = ""

    // if (files.length > 0) {
    //     // Apply CSS class when files are selected
    //     uploadDiv.classList.add('hasFiles');

    //     // Display the list of uploaded files
    //     const ul = document.createElement('ul');
    //     for (let i = 0; i < files.length; i++) {
    //         const li = document.createElement('li');
    //         li.textContent = files[i].name;
    //         ul.appendChild(li);
    //     }
    //     filesList.appendChild(ul);
    // } else {
    //     // Remove CSS class if no files are selected
    //     uploadDiv.classList.remove('hasFiles');
    // }
  })

  document
    .getElementById("upload-btn")
    .addEventListener("click", async function async(event) {
      document.getElementById("upload-btn").disabled = true
      document.getElementById("fileInput").disabled = true
      document.getElementById("to-collapse-upload").style.display = "none"
      document
        .getElementById("upload-zone")
        .classList.add("upload-zone-div-disabled")
      document.getElementById("upload-more-files").style.display = "block"

      event.preventDefault()
      console.log("Upload button clicked, about to call upload function.")
      await upload()
    })

  let uploadedCount = 0
  let totalFileCount = 0
  let errorCount = 0
  let progressBarOverall
  let currentUploadCancelled = false
  const maxFileSize = 5 * 1024 * 1024 //2MB
  const uploadingDIV = document.getElementById("upload-click-div")
  const uploadCount = document.getElementById("uploadCount")
  const totalCount = document.getElementById("totalCount")
  const errorCounter = document.getElementById("errorCount")
  const errorTotal = document.getElementById("errorTotal")

  document.getElementById("cancel-upload-btn").addEventListener("click", () => {
    currentUploadCancelled = true
    document.getElementById("cancel-upload-btn").style.display = "none"
    document.getElementById("cancelled").style.display = "inline"
  })

  const uploadReset = () => {
    document.getElementById("upload-parent-wrapper").innerHTML = ""
    document.getElementById("upload-parent-wrapper").innerHTML =
      UploadWrapperChild

    document.getElementById("upload-btn").disabled = false

    fileuplodInit()
  }

  const upload = async () => {
    currentUploadCancelled = false

    uploadedCount = 0
    totalFileCount = 0
    errorCount = 0

    const initialfileList = document.getElementById("fileInput").files
    if (initialfileList.length == 0) return;

    console.log('intilial File List: ', initialfileList)

    let fileArray = Array.from(initialfileList);
    let indicesToRemove = [];
    // for (record of initialfileList) {
    //   if (record.size > maxFileSize) {
    //     console.log('file size exceeded', record.name)
    //     alert(`File Uploaded exceeds limit for:${record.name}`)
    //     alert(`File Uploaded exceeds limit for:${record.name}`)
    //     return;
    //   }
    // }

    for (let i = 0; i < fileArray.length; i++) {
      if (fileArray[i].size > maxFileSize) {
        console.log('file size exceeded', fileArray[i].name);
        alert(`File Uploaded exceeds limit for: ${fileArray[i].name}`);
        indicesToRemove.push(i);
      }
    }

    let fileList = fileArray.filter((file, index) => !indicesToRemove.includes(index));

    console.log('intilial File List: ', fileList)
    // for (let i = 0; i < initialfileList.length; i++) {
    //   if (initialfileList[i].size > maxFileSize) {
    //     console.log('file size exceeded', initialfileList[i].name);
    //     alert(`File Uploaded exceeds limit for: ${initialfileList[i].name}`);
    //     indicesToRemove.push(i);
    //   }
    // }

    // let fileList = initialfileList.filter((file, index) => !indicesToRemove.includes(index));


    if (fileList.length == 0) return

    const total = fileList.length
    totalFileCount = total
    console.log("ssssddfdvdvdvdvdvddvdv", totalFileCount)

    const notificationId = await createNotification(fileList.length)

    uploadCount.innerHTML = uploadedCount
    totalCount.innerHTML = total

    uploadingDIV.style.display = "grid"

    document.getElementById("upload-btn").disabled = true
    document.getElementById("upload-btn").style.display = "none"

    progressBarOverall = document.getElementById("progressBarOverall")

    progressBarOverall.max = total

    for (let i = 0; i < fileList.length; i++) {
      if (currentUploadCancelled) {
        console.log("upload cancelled")
        console.log('cancel count: ', uploadedCount)
        const res = await fetch('http://localhost:8000/abort-upload', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            NotificationId: notificationId,
            CountOfFiles: uploadedCount,
          })
        })

        console.log('abort result: ', res)
        break;
      }

      //selecting individual file
      const uploadedFile = fileList[i]
      const fileHash = await calculateHash(uploadedFile)
      // Database query to check if file exists in db already *****pending
      //If so continue and dont proceed further

      // const file = fileList[i];

      const oldFileName = uploadedFile.name;

      const newName =
        `[${notificationId}]-` + `${fileHash}` + `!@&` + oldFileName.replace(/\s+/g, '')
      const file = new File([uploadedFile], newName, {
        type: uploadedFile.type,
      })

      console.log(fileHash)

      if (file.size > maxFileSize) {
        alert("File Uploaded exceeds limit", file.name)
        continue
      }

      const fileID = file.name + file.type + i

      console.log(file.name)

      try {
        // getUploadLink(file.name).then((link) => {
        //   console.log("link reached", link.presignedUrl)
        //   const response = uploadFileThroughLink(link.presignedUrl, file)
        // })

        const link = await getUploadLink(file.name, file.type)
        console.log('this is link: ', link)
        // if (link == 0) continue;
        const response = await uploadFileThroughLink(link.presignedUrl, file)
        console.log("response is ", response)

        if (response == "success") {
          uploadedCount++
          if (progressBarOverall) {
            progressBarOverall.value = uploadedCount
            uploadCount.innerHTML = uploadedCount
          }

          console.log(
            "Uploaded Count:",
            uploadedCount,
            "\nTotal File Count: ",
            totalFileCount
          )

          if (uploadedCount === totalFileCount && errorCount === 0) {
            document.getElementById("cancel-upload-div").style.display = "none"
            document.getElementById("successful-message").style.display =
              "block"
            console.log("Reached here")
          }
        } else {
          errorCount++
          errorTotal.innerHTML = errorCount
          document.getElementById("cancel-upload-div").style.display = "none"
          errorCounter.style.display = "block"
        }
      } catch (error) {
        errorCount++
        console.error(`Failed to upload file ${file.name}: ${error}`)
      }

      // if (i == fileList.length - 1) {
      //     setTimeout(() => {
      //         document.getElementById('upload-btn').disabled = false;
      //         // document.getElementById('fileInput').value = '';
      //     }, 1000)
      // }
    }

    // setTimeout(() => {
    //
    // }, 20000)
  }

  async function createNotification(fileCount) {
    try {
      const response = await fetch(
        "http://localhost:8000/create-notification",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ fileCount: fileCount }),
        }
      )

      const data = await response.json()
      const notificationId = data["notification_id"]

      console.log("Notification ID:", notificationId)

      return notificationId
    } catch (error) {
      console.error("Error fetching NotificationID:", error)
    }
  }

  const getUploadLink = async (filename) => {
    console.log(`this is filename, ${filename}`)
    const requestData = {
      name: filename,
    }

    try {
      const response = await fetch("http://localhost:8000/presignedUrl/", {
        method: "POST", // Change the method to POST
        headers: {
          "Content-Type": "application/json", // Specify the Content-Type
        },
        body: JSON.stringify({ input: filename }),
      })

      if (!response.ok) {
        throw new Error("Network response was not ok")
        errorCount++
      }

      const data = await response.json()
      console.log('inside the link getter function: ', data)
      return data
    }
    catch (error) {
      console.error("There was a problem with the fetch operation:", error)
      errorCount++
      return 0;
    }

  }

  const uploadFileThroughLink = async (url, file) => {

    console.log('inside uploadfile: ', url)

    // const formdata = new FormData();

    // formdata.append('file', file)

    try {
      console.log('this is link: ', url)
      const data = await fetch(url, {
        method: "PUT",
        body: file,
      })

      console.log(data)

      if (data.status === 200) {
        return "success"
      } else {
        return "error"
      }
    } catch (error) {
      console.error(error)
      throw Error()
    }
  }

  // aws ke liye upload function


  // const getUploadLink = async (filename, filetype) => {
  //   console.log(`this is filename, ${filename}`)
  //   // const requestData = {
  //   //   name: filename,
  //   // }

  //   try {
  //     const response = await fetch("http://localhost:8000/presignedUrl/", {
  //       method: "POST", // Change the method to POST
  //       headers: {
  //         "Content-Type": "application/json", // Specify the Content-Type
  //       },
  //       body: JSON.stringify({ object_name: filename, file_type: filetype }),
  //     })

  //     if (!response.ok) {
  //       throw new Error("Network response was not ok")
  //       errorCount++
  //     }

  //     const data = await response.json()
  //     console.log('inside the link getter function: ', data)
  //     return data
  //   }
  //   catch (error) {
  //     console.error("There was a problem with the fetch operation:", error)
  //     errorCount++
  //     return 0;
  //   }

  // }


  // const uploadFileThroughLink = async (presignedPostData, file) => {

  //   console.log('this is upload data :', presignedPostData)

  //   // const formdata = new FormData();

  //   // formdata.append('file', file)

  //   try {
  //     const formData = new FormData();
  //     Object.keys(presignedPostData.fields).forEach(key => {
  //       formData.append(key, presignedPostData.fields[key]);
  //     });
  //     formData.append('file', file);

  //     const uploadResponse = await fetch(presignedPostData.url, {
  //       method: 'POST',
  //       body: formData
  //     });

  //     if (uploadResponse.ok) {
  //       alert('File uploaded successfully.');
  //       return 'success';
  //     } else {
  //       alert('Failed to upload file.');
  //       return 'failure';
  //     }
  //   }
  //   catch (error) {
  //     console.error(error)
  //     throw Error()
  //   }

  //   // try {
  //   //   console.log('this is link: ', url)
  //   //   const data = await fetch(url, {
  //   //     method: "PUT",
  //   //     body: file,
  //   //   })

  //   //   console.log(data)

  //   //   if (data.status === 200) {
  //   //     return "success"
  //   //   } else {
  //   //     return "error"
  //   //   }
  //   // } catch (error) {
  //   //   console.error(error)
  //   //   throw Error()
  //   // }
  // }

  // const uploadFileThroughLink = async (presignedPostData, file) => {

  //   try {
  //     console.log('this is upload data :', presignedPostData)

  //     const form = new FormData();
  //     // const fileStream = fs.createReadStream(file.name);


  //     // Append presigned fields to the form data
  //     // for (const key in presignedPostData.fields) {
  //     //   form.append(key, presignedPostData.fields[key]);
  //     // }

  //     Object.keys(presignedPostData.fields).forEach(key => {
  //       form.append(key, presignedPostData.fields[key]);
  //     });

  //     form.append('file', file);

  //     // Upload the file using the presigned URL
  //     response = await axios.post(presignedPostData.url, form)
  //     console.log(`File upload HTTP status code: ${response.status}`);
  //     return response.status;
  //   }

  //   catch (error) {
  //     console.error('File upload failed:', error);
  //     return 400;
  //   }
  // }

  function calculateHash(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader()
      reader.onload = (event) => {
        const arrayBuffer = event.target.result
        const hash = sha256(new Uint8Array(arrayBuffer))
        resolve(hash)
      }
      reader.onerror = (error) => {
        reject(error)
      }
      reader.readAsArrayBuffer(file)
    })
  }

  function sha256(arrayBuffer) {
    const wordArray = CryptoJS.lib.WordArray.create(arrayBuffer)
    return CryptoJS.SHA256(wordArray).toString(CryptoJS.enc.Hex)
  }

  document.getElementById("continue-upload").addEventListener("click", () => {
    console.log("continue clicked")
    document.getElementById("dialog").showModal()
    document.getElementById("continue-upload").style.display = "none"
  })

  document
    .getElementById("upload-minimize-icon")
    .addEventListener("click", () => {
      console.log("minmize clicked")
      document.getElementById("dialog").close()
      document.getElementById("continue-upload").style.display = "flex"
    })
}

fileuplodInit()
