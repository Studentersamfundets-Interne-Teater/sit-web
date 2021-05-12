function _setUpCollapsible() {
  var categories = document.getElementsByClassName("production-categories");
  var productionInfo = document.getElementById("production-info");

  if (window.innerWidth < 1024) {
    for (category of categories) {
      category.nextElementSibling.style.visibility = "hidden";
      category.addEventListener("click", function () {
        this.classList.toggle("active");
        var content = this.nextElementSibling;
        var contentIsActive = this.classList.contains("active");
        if (contentIsActive) {
          content.style.maxHeight = content.scrollHeight + "px";
          content.style.visibility = "visible";
        } else {
          // Wait 200 ms before hiding content for smoother UX
          window.setTimeout(() => {
            content.style.maxHeight = null;
            content.style.visibility = "hidden";
          }, 200);
        }
      });
    }
  } else {
    var emtpyHeight = productionInfo.getBoundingClientRect().height;
    categories[0].nextElementSibling.style.display = "block";
    var initialHeight = categories[0].nextElementSibling.scrollHeight;
    categories[0].nextElementSibling.style.maxHeight = initialHeight + "px";
    console.log(initialHeight);
    if (initialHeight > emtpyHeight) {
      productionInfo.style.height = initialHeight + "px";
    }
    categories[0].style.fontWeight = "600";
    for (var i = 0; i < categories.length; i++) {
      categories[i].addEventListener("click", function (e) {
        e.target.classList.add("active");
        var content = e.target.nextElementSibling;
        e.target.style.fontWeight = "600"; // Bold font when active
        for (category of categories) {
          if (category.nextElementSibling !== content) {
            category.nextElementSibling.style.display = "none";
            category.style.fontWeight = "400"; // Normal font weight
            category.classList.remove("active");
          }
        }
        content.style.display = "block";
        content.style.maxHeight = content.scrollHeight + "px";
        console.log(content.scrollHeight);
        if (content.scrollHeight > emtpyHeight) {
          console.log("Here");
          productionInfo.style.height = content.scrollHeight + "px";
        } else {
          productionInfo.style.height = null;
        }
      });
    }
  }
}

window.addEventListener('load', _setUpCollapsible);