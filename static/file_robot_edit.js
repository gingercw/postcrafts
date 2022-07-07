        
        
const splitPageUrl = window.location.href.split("/");
const cardId = splitPageUrl.slice(-1).pop()


fetch(`/edit_card/details/${cardId}`) 
.then((response) => response.json())
.then((cardInfo) => {

const { TABS, TOOLS } = window.FilerobotImageEditor;
const handleSave = (editedImageObject, designState) => {
  console.log('saved', editedImageObject, designState)
  const cardData = {
    card_id: cardInfo.card_id,
    rawImage: editedImageObject.imageBase64,
  };


  fetch(`/save_edits`, {
    method: 'POST',
    body: JSON.stringify(cardData),

    headers: {
      'Content-Type': 'application/json',
    },
  })
    .then((response) => response.text())
    .then((responseText) => window.location.href = `/`);

}



const config = {
  
  source: cardInfo.card_url,

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
  });})