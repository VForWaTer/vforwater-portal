//Search
function closeSearch() {

    document.getElementById("search_box").outerHTML = "<a href='#' onclick='open_search()' id='srch_box' " +
        "class='w3-hover-white'><i class='fa fa-search fa-fw'></i>  Search</a>";
    document.getElementById("search_but").outerHTML = "<a id='srch_but' class='w3-hover-none'></a>";
    document.getElementById("search_close_but").outerHTML = "<a id='srch_close_but' class='w3-hover-none'></a>";
}

function search_open() {
    if (!document.getElementById("search_box")) {
        var searchBox = document.getElementById("srch_box");
        searchBox.outerHTML = "<a class='w3-hover-none' style='height:1px' id='search_box'><input type='search' " +
            "value='' placeholder='Search ...' style='height:0px; font-size:85%; margin-top:-6px;'></a>";

        var searchBut = document.getElementById("srch_but");
        searchBut.outerHTML = "<a href='#' class='w3-hover-white' style='height:72px' id='search_but' " +
            "onclick='closeSearch()'><i class='fa fa-search fa-fw'></i></a>";

        var closeBut = document.getElementById("srch_close_but");
        closeBut.outerHTML = "<a href='javascript:void(0)' class='w3-hover-white' style='height:72px' " +
            "id='search_close_but' onclick='closeSearch()'><i class='fa fa-remove fa-fw'></i></a>";
    }
}


