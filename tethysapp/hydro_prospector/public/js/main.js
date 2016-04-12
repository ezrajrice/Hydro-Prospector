//Global setTimeout variables so that it can be cleared
var timeoutRefresh = null;
var timeoutInitial = null;

// Load the table on running home.html - give it a timeout and have it run refresh to see if there are any Pending statuses
$( "#forProjectTable" ).load( "/apps/hydro-prospector/all_groups/project-table/", function() {
      timeoutInitial = setTimeout(function () {refresh(); }, 10000);
});

// When user changes the group, clear any active timeouts and run a page load and refresh to check the statuses
$("#select_group").change(function () {
    var owner = $(this).val();
    clearTimeout(timeoutInitial);
    clearTimeout(timeoutRefresh);
    $( "#forProjectTable" ).load( "/apps/hydro-prospector/"+owner+"/project-table/", function() {
      timeoutInitial = setTimeout(function () {refresh(); }, 10000);
    });
});

//Used to validate mandatory fields
function set_delete_url(url) {
    $('.modal-footer a').attr('href', url);
}

// Generate a GIF that covers page while loading
function showProcessing() {

    var divShow = document.createElement("showBackground");
    var imageShow = document.createElement("showImage");
    var elem = document.createElement("img");

    divShow.id = 'showBackground';
    divShow.className="center-parent";
    document.body.appendChild(divShow);
    imageShow.id = 'showImage';
    document.getElementById("showBackground").appendChild(imageShow);
    elem.setAttribute("src", "/static/hydro_prospector/images/loading.gif");
    elem.setAttribute("height", "50");
    elem.setAttribute("width", "400");
    elem.setAttribute("alt", "Upload");
    document.getElementById("showImage").appendChild(elem);
}

// Redirect to home onclick of Yes, Delete it
function redirectDelete() {
    var url = $('#confirmDeleteModalBtn').attr('href');
    showProcessing();
    $.ajax({
      'url': url,
    });

    setTimeout(function() {
        window.location.replace("/apps/hydro-prospector");
    }, 1000);
}

