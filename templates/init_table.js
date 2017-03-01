$(document).ready( function() {
  $('#example').dataTable( {
        "paging": false,
        "bInfo" : false,
        "fixedHeader": true,
    "aoColumnDefs": [
      $searchable_columns
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