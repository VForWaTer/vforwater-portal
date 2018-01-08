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

//Get the User Selection in Workspace
function show_data() {
    var workspaceData = document.getElementById('workdata').value;
	if (workspaceData !== "[]"){
		workspaceData = workspaceData.slice(workspaceData.indexOf("'"), workspaceData.lastIndexOf("'"));
		workspaceData = workspaceData.replace(/'/g, "");
	    workspace_button({'workspaceData': workspaceData.split(", ")})}
}

function workspace_button(json) {
    if (json !== undefined) {
        $.each(json['workspaceData'], function (key, value) {
            // check which buttons already exist before creating a new one:
            if (document.getElementById(value) === null) {
            	var removeValues = "'" + value + "'"
				document.getElementById("workspace").innerHTML += '<li class="respo-padding" id="' + value + '">' +
					'<span class="respo-medium">' + value + '</span><a href="javascript:void(0)"' +
					'onclick="remove_data('+removeValues+')"; class="respo-hover-white respo-right"><i ' +
					'class="fa fa-remove fa-fw"></i></a><br></li>';
            }
        })
    }
}

var csrf_token = getCookie('csrftoken');
// Remove data / elements from workspace
function remove_data(removeData) {
    // remove data from portal:
    document.getElementById(removeData).remove()
    // remove data from session:
    $.ajax({
        url: "/vfwheron/menu",
        datatype: 'json',
        data: {
            remover: removeData,
            'csrfmiddlewaretoken': csrf_token,
        }, // data sent with the post request
        success: function (json) {
        },
    });
//    document.getElementById("workspace").innerHTML += "<li class='respo-padding' id='"+selectedData+"'><span class='respo-medium'>"+selectedData+"</span><a href='javascript:void(0)' onclick=this.parentElement.remove(); class='respo-hover-white respo-right'><i class='fa fa-remove fa-fw'></i></a><br></li>";
}