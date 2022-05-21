
// get random photos from Unsplash API

function chooseImage(evt)
{
  const selectedImage = evt.target.src;
  console.log(selectedImage)

const { TABS, TOOLS } = window.FilerobotImageEditor;
const handleSave = (editedImageObject, designState) => {
  console.log('saved', editedImageObject, designState)
  const cardData = {
    title: prompt("Give your card a name."),
    card_url: editedImageObject.imageBase64,
  };


  fetch(`/save`, {
    method: 'POST',
    body: JSON.stringify(cardData),
    headers: {
      'Content-Type': 'application/json',
    },
  })
    .then((response) => response.json())
    .then((responseJson) =>{
    });

}
const config = {
  source: selectedImage,

  onSave: handleSave,

  annotationsCommon: {
    fill: '#ff0000'
  },
  Text: { text: 'Greetings from ...' },
  Crop: {
    presetsItems: [
      {
        titleKey: 'classicTv',
        descriptionKey: '4:3',
        ratio: 4 / 3,
        // icon: CropClassicTv, // optional, CropClassicTv is a React Function component. Possible (React Function component, string or HTML Element)
      },
      {
        titleKey: 'cinemascope',
        descriptionKey: '21:9',
        ratio: 21 / 9,
        // icon: CropCinemaScope, // optional, CropCinemaScope is a React Function component.  Possible (React Function component, string or HTML Element)
      },
    ],
   
  },
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


document.querySelector('#get_photos button').addEventListener('click', (evt) => {
  const place = document.querySelector('#location').value;
  evt.preventDefault();
  fetch(`/photos?location=${place}`)
    .then((response) => response.json())
    .then((results) => {

      for (const i in results) {
        const imageUrl = results[i].urls.thumb;
        const photoCredit = results[i].user.username;
        const alt_description = results[i].alt_description;
        document
        .querySelector('#photo_choices')
        .insertAdjacentHTML('beforeend', `<div><img width="100" class="choice" alt="${alt_description}" src=${imageUrl}">
        <p>Credit: ${photoCredit}</p></div>`);
      }
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

  onSave: (editedImageObject, designState) => console.log('saved', editedImageObject, designState),
  annotationsCommon: {
    fill: '#ff0000'
  },
  Text: { text: 'Greetings from ...' },
  Crop: {
    presetsItems: [
      {
        titleKey: 'classicTv',
        descriptionKey: '4:3',
        ratio: 4 / 3,
        // icon: CropClassicTv, // optional, CropClassicTv is a React Function component. Possible (React Function component, string or HTML Element)
      },
      {
        titleKey: 'cinemascope',
        descriptionKey: '21:9',
        ratio: 21 / 9,
        // icon: CropCinemaScope, // optional, CropCinemaScope is a React Function component.  Possible (React Function component, string or HTML Element)
      },
    ],
   
  },
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
