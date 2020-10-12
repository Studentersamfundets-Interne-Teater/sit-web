const setHeroImage = () => {
  const heroDiv = document.getElementById("hero");
  const heroImage = document.getElementById("hero-image");
  const portraitImageSource = heroImage.dataset.portrait;
  const landscapeImageSource = heroImage.dataset.landscape;

  const heroWidth = heroDiv.offsetWidth;
  const heroHeight = heroDiv.offsetHeight;
  const landscape = heroWidth >= heroHeight;
  
  console.debug(landscape);

  if (landscape) {
    heroImage.src = landscapeImageSource;
  } else {
    heroImage.src = portraitImageSource;
  }
}

setHeroImage();
window.addEventListener('resize', setHeroImage);