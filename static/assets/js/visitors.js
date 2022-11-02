 
$(document).ready(function () {
    $('#visitors').DataTable();
});
 


$('input.typeahead').typeahead({  
  source:  function (query, process) {  
   console.log( query);
  }  
});  