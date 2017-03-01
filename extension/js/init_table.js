$(document).ready( function() {
  $('#example').dataTable( {
        "paging": false,
        "bInfo" : false,
        "fixedHeader": true,
    "aoColumnDefs": [
      { "bSearchable": true, "aTargets": [ 0 ] }, { type: "non-empty", "bSearchable": false, "aTargets": [ 1 ] }, { type: "non-empty", "bSearchable": false, "aTargets": [ 2 ] }, { type: "non-empty", "bSearchable": false, "aTargets": [ 3 ] }, { type: "non-empty", "bSearchable": false, "aTargets": [ 4 ] }, { type: "non-empty", "bSearchable": false, "aTargets": [ 5 ] }, { type: "non-empty", "bSearchable": false, "aTargets": [ 6 ] }, { type: "non-empty", "bSearchable": false, "aTargets": [ 7 ] }
    ] } );
} );


jQuery.extend( jQuery.fn.dataTableExt.oSort, {
    "non-empty-asc": function (str1, str2) {
        if(str1 == "")
            return 1;
        if(str2 == "")
            return -1;
        str1 = parseFloat(str1)
        str2 = parseFloat(str2)
        return ((str1 < str2) ? -1 : ((str1 > str2) ? 1 : 0));
    },
 
    "non-empty-desc": function (str1, str2) {
        if(str1 == "")
            return 1;
        if(str2 == "")
            return -1;
        str1 = parseFloat(str1)
        str2 = parseFloat(str2)
        return ((str1 < str2) ? 1 : ((str1 > str2) ? -1 : 0));
    }
} );