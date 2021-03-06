


// get random photos from Unsplash API

function chooseImage(evt)
{
  const selectedImage = evt.target.src;
  
  const { TABS, TOOLS } = window.FilerobotImageEditor;
  const handleSave = (editedImageObject, designState) => {
  console.log('saved', editedImageObject, designState)
  const cardData = {
    title: prompt("Give your card a name."),
    rawImage: editedImageObject.imageBase64,
  };


  fetch(`/save`, {
    method: 'POST',
    body: JSON.stringify(cardData),

    headers: {
      'Content-Type': 'application/json',
    },
  })
    .then((response) => response.text())
    .then((responseText) => window.location.href = `./`);


}
const config = {
  source: selectedImage,

  onSave: handleSave,

  defaultSavedImageType: "webp",

  annotationsCommon: {
    fill: '#ff0000'
  },

  Text: { text: 'Add text here...' },
  
  
  tabsIds:
  
  [TABS.ADJUST, TABS.ANNOTATE, TABS.FILTERS, TABS.FINETUNE], // or ['Adjust', 'Annotate', 'Watermark']
  defaultTabId: TABS.ANNOTATE, // or 'Annotate'
  defaultToolId: TOOLS.TEXT, // or 'Text'
};

// Assuming we have a div with id="editor_container"
const filerobotImageEditor = new FilerobotImageEditor(
  document.querySelector('#editor_container'),
  config
);

filerobotImageEditor.render({
  onClose: (closingReason) => {
    console.log('Closing reason', closingReason);
    filerobotImageEditor.terminate();
  }
});
};


document.querySelector('#findPhotos').addEventListener('click', (evt) => {
  const photoQuery = document.querySelector('#photoQuery').value;
  
  document.querySelector('.MultiCarousel-inner').innerHTML = "";
  
  
  fetch(`/photos?photo_query=${photoQuery}`) 
    .then((response) => response.json())
    .then((results) => {
      document.querySelector('#photo_choices').style.display = '';

      for (const i in results) {
        const imageUrl = results[i].urls.raw + "?q=85fm=jpg&w=1000&fit=max";
        const photoCredit = results[i].user.username;
        const alt_description = results[i].alt_description;
        document.querySelector('.MultiCarousel-inner')
        .insertAdjacentHTML('beforeend', 
        `<div class="item">
            <div class="pad15">
            <img width="100" class="choice" alt="${alt_description}" src=${imageUrl}">
            <p>Credit: ${photoCredit}</p>
            </div>
        </div>`
       );
      }

      window.ResCarouselSize();

      
      

      const images = document.querySelectorAll(".choice")
      console.log(images)
      for (const image of images) {
        console.log(image)
        image.addEventListener('click', chooseImage)
      }
    });
});






const { TABS, TOOLS } = window.FilerobotImageEditor;
const config = {
  source: "https://cdn.pixabay.com/photo/2014/04/07/18/44/border-318820_960_720.png",

  defaultSavedImageType: "webp",

  annotationsCommon: {
    fill: '#ff0000'
  },

  Text: { text: 'Add text here...' },
  
  tabsIds:
  
  [TABS.ADJUST, TABS.ANNOTATE, TABS.FILTERS, TABS.FINETUNE], // or ['Adjust', 'Annotate', 'Watermark']
  defaultTabId: TABS.ANNOTATE, // or 'Annotate'
  defaultToolId: TOOLS.TEXT, // or 'Text'
};

// Assuming we have a div with id="editor_container"
const filerobotImageEditor = new FilerobotImageEditor(
  document.querySelector('#editor_container'),
  config
);

filerobotImageEditor.render({
  onClose: (closingReason) => {
    console.log('Closing reason', closingReason);
    filerobotImageEditor.terminate();
  }
});



