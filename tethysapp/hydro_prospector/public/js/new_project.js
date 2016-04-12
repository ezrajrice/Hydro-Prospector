/********************************************************************************
 * Name: new_project.js
 * Author: erice
 * Created On: April 4, 2016
 * License:
 ********************************************************************************/

function add_project_success(data) {
    console.log('Submit AJAX working', data);
}

function add_project_error(data) {
   console.log('Submit not working');
}


//Using Ajax, validate the form, submit, and redirect to home page
$('#submit-add-project').click(function() {
    var form = $('#uploadForm').ajaxForm({
        success: add_project_success,
        uploadProgress: uploadProgressFunction,
        beforeSend: showProcessing,
    });


    if ( validateForm() ) {
      // when its true
      form.submit();
      console.log('Success');
    } else {
     // when its false
     console.log('Fail');
     return false;
    }
});

//Used to validate mandatory fields
function validateForm() {
    var name = document.forms["uploadForm"]["inputName"].value;
    var div_name_input = document.getElementById("div_name_input")
    var div_no_name= document.getElementById("div_no_name")

    // Test both entered name and file to see if they are populated
    if (name == null || name == "") {
        div_no_name.setAttribute("style", "display: block;");
        div_name_input.setAttribute("class", "form-group has-error");
        return false;
    }

    if (name != null || name != "") {
        div_no_name.setAttribute("style", "display: none;");
        div_name_input.setAttribute("class", "form-group");
        return true;
    }
}

// Redirects user to home page on 100 percent load
function uploadProgressFunction(event, position, total, percentComplete) {
    if (percentComplete == 100) {
        setTimeout(function(){
            window.location.replace("../");
        }, 2500);
    }
}
