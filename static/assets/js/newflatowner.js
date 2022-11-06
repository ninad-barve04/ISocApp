$('input.owernername').typeahead({  
    source:  function (query, process) {  
    return $.getJSON('/person/owner', { query: query }, function (response) {  
            console.log(response);  
            return process( response);
        });  
    },
    updater: function(selection){
        console.log("You selected: " + selection)
        $("#ownerid").val(selection.person_ID);
        return selection;
    }
});


$( function() {
    $( "#datepicker" ).datepicker();
    $( "#datepicker" ).datepicker("option", "dateFormat","dd/mm/yy");
  } );