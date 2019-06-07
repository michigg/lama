// make the table a dataTable and show all entries by default
const TABLE_CLASS = '.data-table';
const TABLE_CLASS_NO_PAGING = '.data-table-npaging';

$(document).ready(function () {
    // Bottstrap Toast
    $('.toast').toast('show');

    //Datatables
    const data_table = $(TABLE_CLASS).DataTable({
        "paging": true,
        "pageLength": 10,
        "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "Alle"]],
        // "sPaginationType": "custom",
        "dom": 'lt<"mb-3 float-left" i><"float-right"p><"clearfix">',
        "oLanguage": {
            "sEmptyTable": "Keine Daten verfügbar",
            "sInfo": "_START_ - _END_ von _TOTAL_",
            "sInfoEmpty": "Keine Eintäge gefunden",
            "sLengthMenu": "Zeige _MENU_ Einträge",
            "oPaginate": {
                "sFirst": "First page",
                "sLast": "Last page",
                "sNext": "<i class=\"fas fa-arrow-alt-circle-right\"></i>",
                "sPrevious": "<i class=\"fas fa-arrow-alt-circle-left\"></i>",
            },
            "oAria": {
                "sSortAscending": " - click/return to sort ascending",
                "sSortDescending": " - click/return to sort descending",
            },
        },
        rowReorder: {
            selector: 'td:nth-child(2)'
        },
        responsive: true
    });
    $('#data-table-search-input').keyup(function () {
        data_table.search($(this).val()).draw();
    });

    $("#delete-all-checkbox").change(function () {
        if (document.getElementById('delete-all-checkbox').checked) {
            $('.multiple-select-checkbox').prop("checked", true);
        } else {
            $('.multiple-select-checkbox').prop("checked", false);
        }
    });

    $(".menu-toggle").click(function () {
        $(".wrapper").toggleClass("toggled");
    });


    $('form').submit(function () {
        data_table.search('').draw();
        data_table.rows().nodes().page.len(-1).draw(false);
        $('#data-table-search-input input').val('');
        return true; // return false to cancel form action
    });
});