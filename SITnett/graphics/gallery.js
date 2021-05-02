let galleryItems = document.querySelectorAll('.galleryItem');

const closeLightBox = (galleryItem, overlay) => {
    let originLinkTag = galleryItem.querySelector('a');
    let image = overlay.querySelector('img');
    let caption = overlay.querySelector('figcaption');    
    
    // move image and caption back to their original parents
    originLinkTag.appendChild(image);
    galleryItem.appendChild(caption);
    
    document.body.removeChild(overlay)
}

const openLightBox = (galleryItem) => {
    let lightBoxOverlay = document.createElement('div');
    lightBoxOverlay.classList.add('lightBoxOverlay');

    let lightBoxClose = document.createElement('a');
    lightBoxClose.innerText = 'X';
    lightBoxClose.classList.add('closeButton');
    lightBoxOverlay.appendChild(lightBoxClose);    

    // create image container
    let lightBoxImageContainer = document.createElement('figure');
    lightBoxImageContainer.classList.add('container');
    lightBoxOverlay.appendChild(lightBoxImageContainer);

    // move image to overlay
    let image = galleryItem.querySelector('img');
    lightBoxImageContainer.appendChild(image);
    
    // move figcaption
    let caption = galleryItem.querySelector('figcaption');
    lightBoxImageContainer.appendChild(caption);
    
    // add closing routine
    lightBoxClose.addEventListener('click', (e) => {
        e.preventDefault();
        closeLightBox(galleryItem, lightBoxOverlay);
    });
    
    // display overlay
    document.body.appendChild(lightBoxOverlay);
}

galleryItems.forEach(el => {
    let linkTag = el.querySelector('a');
    linkTag.addEventListener('click', (e) => {
        e.preventDefault();
        openLightBox(el);
    });
});