function openNav() {
  document.getElementById("mySidebar").style.width = "250px";
}

function closeNav() {
  document.getElementById("mySidebar").style.width = "0";
}

// hide other form tabs and show the one that is clicked
function showForm(form) {
  if (form == "api") {
    document.getElementById("api").classList.add("active");
    document.getElementById("api").style.display = "block";
    document.getElementById("types").style.display = "none";
    document.getElementById("random").style.display = "none";
  }
  else if (form == "types") {
    document.getElementById("types").classList.add("active");
    document.getElementById("api").style.display = "none";
    document.getElementById("types").style.display = "block";
    document.getElementById("random").style.display = "none";
  }
  else {
    document.getElementById("random").classList.add("active");
    document.getElementById("api").style.display = "none";
    document.getElementById("types").style.display = "none";
    document.getElementById("random").style.display = "block";
  }
}

