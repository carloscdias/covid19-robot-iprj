function format(d) {
    return '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">' +
        '<tr>' +
        '<td>Resumo:</td>' +
        '<td>' + d.resumo + '</td>' +
        '</tr>' +
        '<tr>' +
        '</table>';
}

function filterColumn ( i ) {
    $('#example').DataTable().column( i ).search(
        $('#col'+i+'_filter').val(),
        $('#col'+i+'_regex').prop('checked'),
        $('#col'+i+'_smart').prop('checked')
    ).draw();
}

$(document).ready(function() {
    var table = $('#example').DataTable({
        "ajax": "/novidade/json/",
        "columns": [{
                "className": 'details-control',
                "orderable": false,
                "data": null,
                "defaultContent": ''
            },
            {"data": "titulo"},
            {"data": "idioma"},
            {"data": "autores"},
            {"data": "categoria"},
            {"data": "jornal"},
            {"data": "dataPrimeiroAcesso"},
            {"data": "data_publicacao"},
            {
                "data": "fonte",
                "render": function(data, type, row, meta) {
                    return '<a href="' + data + '">Acessar</a>';
                }
            },
            {
                "data": "link_externo",
                "render": function (data, type, row, meta) {
                    return '<a target="_blank" href="'+data+'">Acessar</a>';
                }
            },
        ],
        "order": [[5, "desc"]],
        "autoWidth": false,
        "columnDefs": [
                { "width": "2%", "targets": 0 },
                { "width": "6%", "targets": 6 },
        ],
    });

    $('input.column_filter').on( 'keyup click', function () {
        filterColumn( $(this).parents('tr').attr('data-column') );
    } );
    // Add event listener for opening and closing details
    $('#example tbody').on('click', 'td.details-control', function() {
        var tr = $(this).closest('tr');
        var row = table.row(tr);

        if (row.child.isShown()) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        } else {
            // Open this row
            row.child(format(row.data())).show();
            tr.addClass('shown');
        }
    });
});