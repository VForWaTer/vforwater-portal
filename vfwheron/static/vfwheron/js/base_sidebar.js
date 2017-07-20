//Toggle between showing and hiding the sidenav, and add overlay effect
function respo_open() {
	// Get the Sidenav
	var mySidenav = document.getElementById("mySidenav");

	// Get the DIV with overlay effect
	var overlayBg = document.getElementById("myOverlay");

	if (mySidenav.style.display === "block") {
		mySidenav.style.display = "none";
		overlayBg.style.display = "none";
	} else {
		mySidenav.style.display = "block";
		overlayBg.style.display = "block";
	}
}

//Close the sidenav with the close button
function respo_close() {
	var mySidenav = document.getElementById("mySidenav");

	var overlayBg = document.getElementById("myOverlay");

	mySidenav.style.display = "none";
	overlayBg.style.display = "none";
}