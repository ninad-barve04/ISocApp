$('input.visiting').typeahead({  
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
        $("#visting_member_id").val(selection.person_ID);
        $('#visting_flat_id').val(selection.flat_ID);

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
    }  ,
    displayText: function(item){
        if( item.selected){
            return `${item.phone_number} `;
        }
        return `${item.name}-${item.phone_number} `;
    },
    updater: function(selection){
        console.log("You selected: " + selection)
        $("#vph").val(selection.phone_number);
        $('#person_name').val(selection.name);
        $('#visitor_id').val(selection.person_ID);

        selection['selected'] = true;
        // fetch the flat owned by 

        return selection;
    }
});