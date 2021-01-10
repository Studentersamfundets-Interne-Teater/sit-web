function galleryNavigation(imgs) {
    var expandImg = document.getElementById("expandedImg");
    var imgText = document.getElementById("imgtext");
    expandImg.src = imgs.src;
    imgText.innerHTML = imgs.alt;
  }

let imageList = document.getElementsByClassName("gallery-nav");
  
//hent data
//rendre data
/*
function renderImageList(data) {
  let html = '';

  for (let i = 0; i < data.length; i++) {
      const img = data[i];
      html += `
        <figure>
          <img src="${img.url}" />
          <figcaption>${img.type}</figcaption>
        </figure>
      `;
  }

  return html;
}*/