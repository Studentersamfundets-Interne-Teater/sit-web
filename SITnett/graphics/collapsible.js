var categories = document.getElementsByClassName("production-categories");

if (window.innerWidth < 1024) {
  for (category of categories) {
    category.nextElementSibling.style.visibility = "hidden";
    category.addEventListener("click", function() {
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
}

else {
  categories[0].nextElementSibling.style.display = "block";
  categories[0].style.fontWeight = "600";
  for (i = 0; i < categories.length; i++) {
    categories[i].addEventListener("click", function() {
      this.classList.add("active");
      var content = this.nextElementSibling; 
      this.style.fontWeight = "600"; // Bold font when active
      for (category of categories) {
        if (category.nextElementSibling !== content) {
          category.nextElementSibling.style.display = "none";
          category.style.fontWeight = "400"; // Normal font weight
          category.classList.remove("active");
        }
      }      
      content.style.display = "block";
      content.style.maxHeight = content.scrollHeight + "px";
    });
  }
  
}
