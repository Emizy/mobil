$(document).ready(function () {

    let supplier_quotation_tbl = $("#supplier_quotation_tbl").DataTable({
        "dom": '<"top"Brt><"bottom"ip><"clear">',
        "processing": true,
        "serverSide": true,
        lengthChange: !1,
        responsive: true,
        "pageLength": 100,
        "searching": true,
        "paging": true,
        ajax: {
            "url": '/supplier/quotation/',
            'type': 'POST',
            'data': {
                'csrfmiddlewaretoken': $("[name=csrfmiddlewaretoken]").val(),
                columnsDef: [
                    'supplier', 'invoice_number', 'invoice_date', 'due_date', 'amount', 'status', 'created_by', 'created_at', ''],
            }
        },
        columns: [
            {"data": "supplier", "autoWidth": true, "defaultContent": "<i>Not set</i>"},
            {"data": "invoice_number", "autoWidth": true, "defaultContent": "<i>Not set</i>"},
            {"data": "invoice_date", "autoWidth": true, "defaultContent": "<i>Not set</i>"},
            {"data": "due_date", "autoWidth": true, "defaultContent": "<i>Not set</i>"},
            {"data": "amount", "autoWidth": true, "defaultContent": "<i>Not set</i>"},
            {"data": "status", "autoWidth": true, "defaultContent": "<i>Not set</i>"},
            {"data": "created_by", "autoWidth": true, "defaultContent": "<i>Not set</i>"},
            {"data": "created_at", "autoWidth": true, "defaultContent": "<i>Not set</i>"},
            {"data": "", "autoWidth": true, "defaultContent": "<i>Not set</i>"}
        ],
        columnDefs: [
            {
                width: '75px',
                targets: 4,
                orderable: false,
                render: function (data, type, full, meta) {
                    var amount = '₦' + data.toLocaleString();
                    return amount;
                },
            },
            {
                width: '75px',
                targets: 5,
                orderable: false,
                render: function (data, type, full, meta) {
                    let message = ''
                    if (data === 'PENDING') {
                        message = `<span class="badge badge-warning">PENDING</span>`
                    }
                    return message;
                },
            },
            {
                targets: -1,
                title: 'Actions',
                orderable: false,
                render: function (data, type, full, meta) {
                    return '';
                },
            }
        ],
    });
})