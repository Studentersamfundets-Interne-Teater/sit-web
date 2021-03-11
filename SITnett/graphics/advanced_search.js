const advancedParams = document.getElementById("advanced-search");
const advancedSearchBtn = document.getElementById("show-advanced-search-btn");

function main() {
  if (advancedParams) {
    advancedParamsDisplay = localStorage.getItem(
      "advanced-member-params-display"
    );
    if (advancedParamsDisplay) {
      advancedParams.style.display = advancedParamsDisplay;
    } else {
      advancedParams.style.display = "none";
      localStorage.setItem("advanced-member-params-display", "none");
    }

    advancedSearchBtn.addEventListener("click", toggleVisibility);
  }
}

function toggleVisibility() {
  const newDisplay = advancedParams.style.display == "none" ? "block" : "none";
  advancedParams.style.display = newDisplay;
  localStorage.setItem("advanced-member-params-display", newDisplay);
}

main();
