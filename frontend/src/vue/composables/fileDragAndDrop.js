export default (
  dragAreaName, 
  fileUrl, 
  data, 
  fileDataName, 
  acceptedFileType='image',
  videoType=null
) => {
  const dragArea = document.querySelector(`.${dragAreaName}`)
  const dragText = dragArea.querySelector('.js-drag-text')
  
  dragArea.addEventListener('dragover', (event) => {
    event.preventDefault()
    dragText.classList.remove('error')
    dragText.textContent = 'Release to upload'
    dragArea.classList.add('active')
  })

  dragArea.addEventListener('dragleave', () => {
    dragText.textContent = 'Drag & Drop to upload'
    dragArea.classList.remove('active')
  })

  dragArea.addEventListener('drop', (event) => {
    event.preventDefault()
    const file = event.dataTransfer.files[0]

    if (file == undefined) {
      dragText.textContent = `Failed. Please try again.`
      dragText.classList.add('error')
      return
    }

    const fileType = file.type
    const type = fileType.split('/')[0]
    
    if (type != acceptedFileType) {
      dragText.textContent = `File type must be ${acceptedFileType}`
      dragText.classList.add('error')
      dragArea.classList.remove('active')
      return
    }

    if (videoType) {
      videoType.value = fileType
    }

    data[fileDataName] = file
    fileUrl.value = URL.createObjectURL(file)
  })
}