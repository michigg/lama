// make the table a dataTable and show all entries by default
const TABLE_CLASS = '.data-table';

$(document).ready(function () {
    // if ($(TABLE_CLASS)) {
    const data_table = $(TABLE_CLASS).DataTable({
        "lengthMenu": [[-1], ["All"]],
        "dom": 'it'
    });
    // }
    $('#data-table-search-input').keyup(function () {
        data_table.search($(this).val()).draw();
    });

    $("#delete-all-checkbox").change(function () {
        if (document.getElementById('delete-all-checkbox').checked) {
            $('.delete-checkbox').prop("checked", true);
        } else {
            $('.delete-checkbox').prop("checked", false);
        }
    });
});