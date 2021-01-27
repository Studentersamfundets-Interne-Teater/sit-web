var categories = document.getElementsByClassName("production-categories");
var i;

if (window.innerWidth < 1024) {
  for (i = 0; i < categories.length; i++) {
    categories[i].addEventListener("click", function() {
      this.classList.toggle("active");
      var content = this.nextElementSibling;
      if (content.style.maxHeight){
        content.style.maxHeight = null;
      } else {
        content.style.maxHeight = content.scrollHeight + "px";
      } 
      /* if (this.style.maxHeight) {
        this.style.maxHeight = null; 
      } else {
        this.style.maxHeight = this.scrollHeight + "px";
      } */
    });
  }
}

else {
  categories[0].nextElementSibling.style.display = "block";
  categories[0].style.fontWeight = "600";
  for (i = 0; i < categories.length; i++) {
    categories[i].addEventListener("click", function() {
      this.classList.toggle("active");
      var content = this.nextElementSibling; 
      this.style.fontWeight = "600"; //Bold font when active
      for (j = 0; j<categories.length; j++) {
        if (categories[j].nextElementSibling !== content) {
          categories[j].nextElementSibling.style.display = "none";
          categories[j].style.fontWeight = "400"; //Normal font weight
        }
      }      
      content.style.display = "block";
    });
  }
  
}
