$(document).ready( function() {
  $('#example').dataTable( {
        "paging": false,
        "bInfo" : false,
        "fixedHeader": true,
    "aoColumnDefs": [
      { "bSearchable": true, "aTargets": [ 0 ] }, { "bSearchable": false, "aTargets": [ 1 ] }, { "bSearchable": false, "aTargets": [ 2 ] }, { "bSearchable": false, "aTargets": [ 3 ] }, { "bSearchable": false, "aTargets": [ 4 ] }, { "bSearchable": false, "aTargets": [ 5 ] }, { "bSearchable": false, "aTargets": [ 6 ] }, { "bSearchable": false, "aTargets": [ 7 ] }
    ] } );
} );


jQuery.fn.dataTableExt.oSort['numWithNull-asc'] = function(a,b) {
var x = parseInt(a);
var y = parseInt(b);
return ((isNaN(x) || x < y) ? -1 : ((isNaN(y) || x > y) ? 1 : 0));
};
jQuery.fn.dataTableExt.oSort['numWithNull-desc'] = function(a,b) {
var x = parseInt(a);
var y = parseInt(b);
return ((isNaN(x) || x < y) ? 1 : ((isNaN(y) || x > y) ? -1 : 0));
};