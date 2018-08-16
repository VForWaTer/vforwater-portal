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
function show_data(evt) {
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
				document.getElementById("workspace").innerHTML += '<li draggable="true" class="respo-padding task" ' +
                    'data-id="' + key + '" onmouseover="" style="cursor: pointer;" id="' + key + '">' +
					'<span class="respo-medium" title="'+title+'"><div class="task__content">' + btnName + '</div>' +
                    '<div class="task__actions"></div></span><a href="javascript:void(0)"' +
					'onclick="remove_single_data('+key+')"; class="respo-hover-white respo-right">' +
                    '<i class="fa fa-remove fa-fw"></i></a><br></li>';
				/*
				document.getElementById("workspace").innerHTML += '<li draggable="true" class="respo-padding" ' +
					'onmouseover="" style="cursor: pointer;" id="' + key + '" onclick="store_menu(' + key + ')" >' +
					'<span class="respo-medium" title="'+title+'">' + btnName + '</span><a href="javascript:void(0)"' +
					'onclick="remove_single_data('+key+')"; class="respo-hover-white respo-right">' +
                    '<i class="fa fa-remove fa-fw"></i></a><br></li>' +
                    '<div id="w3popup" class="w3popup"><span class="popuptext" id="pop' + key + '"></span></div>' +
            '<li class="task" data-id="1"><div class="task__content">Build An App</div><div class="task__actions">' +
            '</div></li>';*/
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
    delete workspaceData[removeData];
    sessionStorage.setItem("btn", JSON.stringify(workspaceData))
}

function remove_all_datasets() {
	// remove button from portal
	$.each(JSON.parse(sessionStorage.getItem("btn")), function (key) {
		document.getElementById(key).remove()
    });
	// remove button from session
	sessionStorage.removeItem("btn");
}

// code for context menu from https://www.sitepoint.com/building-custom-right-click-context-menu-javascript/
// MIT license

// (function() {

  "use strict";
  //
  // H E L P E R    F U N C T I O N S

  /**
   * Function to check if we clicked inside an element with a particular class
   * name.
   *
   * @param {Object} e The event
   * @param {String} className The class name to check against
   * @return {Boolean}
   */
  function clickInsideElement( e, className ) {
    var el = e.srcElement || e.target;

    if ( el.classList.contains(className) ) {
      return el;
    } else {
      while ( el = el.parentNode ) {
        if ( el.classList && el.classList.contains(className) ) {
          return el;
        }
      }
    }

    return false;
  }

  /**
   * Get's exact position of event.
   *
   * @param {Object} e The event passed in
   * @return {Object} Returns the x and y position
   */
  function getPosition(e) {
    var posx = 0;
    var posy = 0;

    if (!e) var e = window.event;

    if (e.pageX || e.pageY) {
      posx = e.pageX;
      posy = e.pageY;
    } else if (e.clientX || e.clientY) {
      posx = e.clientX + document.body.scrollLeft + document.documentElement.scrollLeft;
      posy = e.clientY + document.body.scrollTop + document.documentElement.scrollTop;
    }

    return {
      x: posx,
      y: posy
    }
  }

  //
  // C O R E    F U N C T I O N S
  //

  /**
   * Variables.
   */
  var contextMenuClassName = "context-menu";
  var contextMenuItemClassName = "context-menu__item";
  var contextMenuLinkClassName = "context-menu__link";
  var contextMenuActive = "context-menu--active";

  var taskItemClassName = "task";
  var taskItemInContext;

  var clickCoords;
  var clickCoordsX;
  var clickCoordsY;

  var menu = document.querySelector("#context-menu");
  console.log('menu: ', menu)
  var menuState = 0;
  var menuWidth;
  var menuHeight;
  var menuPosition;
  var menuPositionX;
  var menuPositionY;

  var windowWidth;
  var windowHeight;

  /**
   * Initialise our application's code.
   */
  function init() {
    contextListener();
    clickListener();
    keyupListener();
    resizeListener();
  }

  /**
   * Listens for contextmenu events.
   */
  function contextListener() {
    document.addEventListener( "contextmenu", function(e) {
      taskItemInContext = clickInsideElement( e, taskItemClassName );

      if ( taskItemInContext ) {
        e.preventDefault();
        toggleMenuOn();
        positionMenu(e);
      } else {
        taskItemInContext = null;
        toggleMenuOff();
      }
    });
  }

  /**
   * Listens for click events.
   */
  function clickListener() {
    document.addEventListener( "click", function(e) {
      var clickeElIsLink = clickInsideElement( e, contextMenuLinkClassName );

      if ( clickeElIsLink ) {
        e.preventDefault();
        menuItemListener( clickeElIsLink );
      } else {
        var button = e.which || e.button;
        if ( button === 1 ) {
          toggleMenuOff();
        }
      }
    });
  }

  /**
   * Listens for keyup events.
   */
  function keyupListener() {
    window.onkeyup = function(e) {
      if ( e.keyCode === 27 ) {
        toggleMenuOff();
      }
    }
  }

  /**
   * Window resize event listener
   */
  function resizeListener() {
    window.onresize = function(e) {
      toggleMenuOff();
    };
  }

  /**
   * Turns the custom context menu on.
   */
  function toggleMenuOn() {
    if ( menuState !== 1 ) {
      menuState = 1;
      console.log('menu: ', menu)
      menu.classList.add( contextMenuActive );
    }
  }

  /**
   * Turns the custom context menu off.
   */
  function toggleMenuOff() {
    if ( menuState !== 0 ) {
      menuState = 0;
      menu.classList.remove( contextMenuActive );
    }
  }

  /**
   * Positions the menu properly.
   *
   * @param {Object} e The event
   */
  function positionMenu(e) {
    clickCoords = getPosition(e);
    clickCoordsX = clickCoords.x;
    clickCoordsY = clickCoords.y;

    menuWidth = menu.offsetWidth + 4;
    menuHeight = menu.offsetHeight + 4;

    windowWidth = window.innerWidth;
    windowHeight = window.innerHeight;

    if ( (windowWidth - clickCoordsX) < menuWidth ) {
      menu.style.left = windowWidth - menuWidth + "px";
    } else {
      menu.style.left = clickCoordsX + "px";
    }

    if ( (windowHeight - clickCoordsY) < menuHeight ) {
      menu.style.top = windowHeight - menuHeight + "px";
    } else {
      menu.style.top = clickCoordsY + "px";
    }
  }

  /**
   * Dummy action function that logs an action when a menu item link is clicked
   *
   * @param {HTMLElement} link The link that was clicked
   */
  function menuItemListener( link ) {
    console.log( "Task ID - " + taskItemInContext.getAttribute("data-id") + ", Task action - " + link.getAttribute("data-action"));
    toggleMenuOff();
  }

  /**
   * Run the app.
   */
  init();

// })();