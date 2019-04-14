// make the table a dataTable and show all entries by default
const TABLE_CLASS = '.data-table';

$(document).ready(function () {
    // if ($(TABLE_CLASS)) {
    const data_table = $(TABLE_CLASS).DataTable({
        "lengthMenu": [[-1], ["All"]],
        "dom": 'it',
        rowReorder: {
            selector: 'td:nth-child(2)'
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