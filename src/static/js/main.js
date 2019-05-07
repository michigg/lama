// make the table a dataTable and show all entries by default
const TABLE_CLASS = '.data-table';

$(document).ready(function () {
    // if ($(TABLE_CLASS)) {
    const data_table = $(TABLE_CLASS).DataTable({
        "lengthMenu": [[-1], ["All"]],
        "bPaginate": true,
        "pageLength": 10,
        // "sPaginationType": "custom",
        "dom": 'itlp',
        // "paginate": {
        //     next: '<i class="fas fa-arrow-alt-circle-right"></i>',
        //     previous: '<i class="fas fa-arrow-alt-circle-left"></i>'
        // },
        rowReorder: {
            selector: true,
        },
        responsive: true,
    });
    // }
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
    })
});