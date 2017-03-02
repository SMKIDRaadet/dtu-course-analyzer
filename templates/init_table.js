$(document).ready( function() {
  $('#example').dataTable( {
        "paging": false,
        "bInfo" : false,
        "fixedHeader": true,
    "aoColumnDefs": [
      $searchable_columns
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