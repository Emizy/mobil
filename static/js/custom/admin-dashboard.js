$(document).ready(function () {

    let supplier_quotation_tbl = $("#supplier_quotation_tbl").DataTable({
        "dom": '<"top"Bfrt><"bottom"ip><"clear">',
        "processing": true,
        "serverSide": true,
        lengthChange: !1,
        responsive: true,
        "pageLength": 100,
        "searching": true,
        "paging": true,
        ajax: {
            "url": '/administrator/quotations/supplier/',
            'type': 'POST',
            'data': {
                'csrfmiddlewaretoken': $("[name=csrfmiddlewaretoken]").val(),
                'status': 'PENDING',
                columnsDef: ['id', 'supplier', 'station_name', 'invoice_number', 'invoice_date', 'due_date', 'amount'],
            }
        },
        columns: [
            {"data": "supplier", "autoWidth": true, "defaultContent": "<i>Not set</i>"},
            {"data": "station_name", "autoWidth": true, "defaultContent": "<i>Not set</i>"},
            {"data": "invoice_number", "autoWidth": true, "defaultContent": "<i>Not set</i>"},
            {"data": "invoice_date", "autoWidth": true, "defaultContent": "<i>Not set</i>"},
            {"data": "due_date", "autoWidth": true, "defaultContent": "<i>Not set</i>"},
            {"data": "amount", "autoWidth": true, "defaultContent": "<i>Not set</i>"}
        ],
        columnDefs: [
            {
                targets: 0,
                orderable: false,
            },
            {
                targets: 1,
                orderable: false,
            },
            {
                width: '75px',
                targets: 5,
                orderable: false,
                render: function (data, type, full, meta) {
                    var amount = '₦' + data.toLocaleString();
                    return amount;
                },
            }
        ],
        fnDrawCallback: function () {

        }
    });
    $(".supplier_quotation_tbl tbody").on("click", "tr", function () {
        var row_id = supplier_quotation_tbl.row(this).data().id;
        window.location.replace(`/administrator/quotations-preview/supplier/${row_id}`)
        // window.location.href = ''
    });
    $('.supplier_quotation_tbl tbody tr').hover(function () {
        $(this).css('cursor', 'pointer');
    }, function () {
        $(this).css('cursor', 'auto');
    });
})