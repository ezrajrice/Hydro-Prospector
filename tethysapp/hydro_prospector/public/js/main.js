//Global setTimeout variables so that it can be cleared
var timeoutRefresh = null;
var timeoutInitial = null;

//Load Project Table
function refresh() {
   // Pulls the active value of the Select Group gizmo and the hidden value of refresh_required
   var select_group = $("#select_group").val();
   var refresh_required = $('#refresh-required').val();
   console.log(refresh_required);

   if (refresh_required) {
      if (timeoutRefresh) {
         clearTimeout(timeoutRefresh);
         timeoutRefresh = null;
        }
      $( "#forProjectTable" ).load( "/apps/hydro-prospector/"+select_group+"/project-table/", function() {
        timeoutInitial = setTimeout(function () {refresh(); }, 50000);
      });
      }
}

// Load the table on running home.html - give it a timeout and have it run refresh to see if there are any Pending statuses
$( "#btnInitApp" ).click(function() {
    var button_bg = document.getElementById("btnInitApp");
    $('#btnInitApp').attr('disabled', true);
    button_bg.style.background="#953232";
    $.ajax({url: "/apps/hydro-prospector/rest/project/initialize-app-settings/", success: function(result){
    $('#btnInitApp').attr('disabled', false)} });
});

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

 //Dynamic querying select2 for SRID
$(".js-query-srid-ajax").select2({
  placeholder: "No Basemap Available If Left Blank",
  allowClear: true,
  ajax: {
    url: "/apps/hydro-prospector/processing/query-srid-by-query/",
    delay: 1000,
    data: function (params) {
      return {
        q: params, // search term
      };
    },
    results: function (data, params) {
      // parse the results into the format expected by Select2
      // since we are using custom formatting functions we do not need to
      // alter the remote JSON data, except to indicate that infinite
      // scrolling can be used
      return {
        results: data.results,
      };
    },

  },
  initSelection: function(element, callback) {
    return $.ajax({
        url: "/apps/hydro-prospector/processing/query-srid-by-id/",
        data: { id: element.val() },
    }).done(function(data) {
      var results;
      results = [];
      results.push({
        id: data['results'][0].id,
        text: data['results'][0].text
      });
      callback(results[0]);
    });
  }
});

$(function(){
  $('.curve-pattern-tab').on('click', function(){
    setTimeout(function() {
      $(window).resize();
      console.log('resize');
     }, 250);

  });
});
