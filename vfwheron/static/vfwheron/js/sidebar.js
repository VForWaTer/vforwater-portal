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

//Toggle between showing and hiding the sidemenu, and add overlay effect
function Sidemenu_open() {
	// Get the Sidemenu
	var mySidemenu = document.getElementById("mySidemenu");

	// Get the DIV with overlay effect
	var overlaymenu = document.getElementById("mySidemenuOverlay");

	if (mySidemenu.style.display === "block") {
		mySidemenu.style.display = "none";
		overlaymenu.style.display = "none";
	} else {
		mySidemenu.style.display = "block";
		overlaymenu.style.display = "block";
	}
}

//Close the sidemenu with the close button
function Sidemenu_close() {
	var mySidemenu = document.getElementById("mySidemenu");

	var overlaymenu = document.getElementById("mySidemenuOverlay");

	mySidemenu.style.display = "none";
	overlaymenu.style.display = "none";
}