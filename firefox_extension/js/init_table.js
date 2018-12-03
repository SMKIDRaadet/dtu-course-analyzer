$(document).ready( function() {
  $('#example').dataTable( {
        "paging": false,
        "bInfo" : false,
        "fixedHeader": true,
    "aoColumnDefs": [
      { "bSearchable": true, "aTargets": [ 0 ] }, { type: "non-empty", "bSearchable": true,"aTargets": [ 1 ] }, { type: "non-empty", "asSorting": [ "desc", "asc" ], "bSearchable": false, "aTargets": [ 2 ] }, { type: "non-empty", "asSorting": [ "desc", "asc" ], "bSearchable": false, "aTargets": [ 3 ] }, { type: "non-empty", "asSorting": [ "desc", "asc" ], "bSearchable": false, "aTargets": [ 4 ] }, { type: "non-empty", "asSorting": [ "desc", "asc" ], "bSearchable": false, "aTargets": [ 5 ] }, { type: "non-empty", "asSorting": [ "desc", "asc" ], "bSearchable": false, "aTargets": [ 6 ] }, { type: "non-empty", "asSorting": [ "desc", "asc" ], "bSearchable": false, "aTargets": [ 7 ] }
    ] } );
} );


function safeParseFloat(n) {
	if(!isNaN(parseFloat(n)) && isFinite(n)){
		return(parseFloat(n))
	} else{
		return(n)
	}
}

jQuery.extend( jQuery.fn.dataTableExt.oSort, {
    "non-empty-asc": function (str1, str2) {
        if(str1 == "")
            return 1;
        if(str2 == "")
            return -1;
        str1 = safeParseFloat(str1)
        str2 = safeParseFloat(str2)
        return ((str1 < str2) ? -1 : ((str1 > str2) ? 1 : 0));
    },
 
    "non-empty-desc": function (str1, str2) {
        if(str1 == "")
            return 1;
        if(str2 == "")
            return -1;
        str1 = safeParseFloat(str1)
        str2 = safeParseFloat(str2)
        return ((str1 < str2) ? 1 : ((str1 > str2) ? -1 : 0));
    }
} );