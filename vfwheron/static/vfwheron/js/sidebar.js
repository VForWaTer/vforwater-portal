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

// Get the User Selection in Workspace
// Button information is stored in an HTML object with Id 'workdata'
// it is stored as a string, so the following function transforms this string to a dictionary again
function show_data() {
    var workspaceData = JSON.parse(sessionStorage.getItem("btn"));
    if (workspaceData !== "[]") {
        workspace_button({'workspaceData': workspaceData})
    }
}

// build buttons in workspace and store selection in clients sessionStorage
function workspace_button(json) {
    if (json !== undefined) {
        $.each(json['workspaceData'], function (key, value) {
            let btnName;
            if (value['name'].length + value['abbr'].length + value['unit'].length <= 14) {
                btnName = value['name'] + ' (' + value['abbr'] + ' in ' + value['unit'] + ') - ' + key;
            } else if (value['name'].length + value['abbr'].length <= 16) {
                btnName = value['name'] + ' (' + value['abbr'] +') - ' + key;
            } else if (value['name'].length <= 18) {
                btnName = value['name'] + ' - ' + key;
            } else {
                btnName = value['abbr'] + ' in ' + value['unit'] + ' - ' + key;
            }
            let title = value['name'] + ' (' + value['abbr'] + ' in ' + value['unit'] + ')';
            // check if buttons already exist before creating a new one:
            if (document.getElementById(key) === null) {
            	var removeValues = "'" + key + "'";
				document.getElementById("workspace").innerHTML += '<li class="respo-padding" id="' + key + '">' +
					'<span class="respo-medium" title="'+title+'">' + btnName + '</span><a href="javascript:void(0)"' +
					'onclick="remove_single_data('+removeValues+')"; class="respo-hover-white respo-right">' +
                    '<i class="fa fa-remove fa-fw"></i></a>' +
                    '<br></li>';
            }
        })
    }
}

// Remove data / elements from workspace
function remove_single_data(removeData) {
    // remove data from portal:
    document.getElementById(removeData).remove();
    // remove data from session:
    var workspaceData = JSON.parse(sessionStorage.getItem("btn"));
    delete workspaceData[removeData]
    sessionStorage.setItem("btn", JSON.stringify(workspaceData))
}

function remove_all_datasets() {
	// remove button from portal
	$.each(JSON.parse(sessionStorage.getItem("btn")), function (key) {
		console.log('remove key: ', key)
		document.getElementById(key).remove()
    });
	// remove button from session
	sessionStorage.removeItem("btn");
}