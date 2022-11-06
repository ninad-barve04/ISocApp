$('input.owner').typeahead({  
    source:  function (query, process) {  
    return $.getJSON('/person/owner', { query: query }, function (response) {  
            console.log(response);  
            return process( response);
        });  
    },
    displayText: function(item){
        return `${item.name} Flat:  ${item.bldg_no}-${item.flat_no}`; 
    },
    updater: function(selection){
        console.log("You selected: " + selection)
        $("#owner_ID").val(selection.person_ID);
        $('#owner_flat_id').val(selection.flat_ID);
       // $('#owner_flat').val(`${selection.bldg_no}-${selection.flat_no}`);

        // fetch the flat owned by 

        return selection;
    }
});

$('input.vph').typeahead({  
    source:  function (query, process) {  
    return $.get('/person/visitor', { query: query }, function (data) {  
            console.log(data);   
            return process(data);  
        });  
    }  
});