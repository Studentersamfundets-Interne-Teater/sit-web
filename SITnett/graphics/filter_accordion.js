function filterFunction() {
  var x = document.getElementById("filter-container");
  if (x.className.indexOf("filter-show") == -1) {
    x.className += " filter-show";
  } else { 
    x.className = x.className.replace(" filter-show", "");
  }
}