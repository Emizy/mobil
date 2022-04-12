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
            "url": '/administrator/quotations/supplier/',
            'type': 'POST',
            'data': {
                'csrfmiddlewaretoken': $("[name=csrfmiddlewaretoken]").val(),
                columnsDef: ['supplier', 'invoice_number', 'invoice_date', 'due_date', 'amount', 'station_name', 'status', 'created_at', ''],
            }
        },
        columns: [
            {"data": "supplier", "autoWidth": true, "defaultContent": "<i>Not set</i>"},
            {"data": "station_name", "autoWidth": true, "defaultContent": "<i>Not set</i>"},
            {"data": "invoice_number", "autoWidth": true, "defaultContent": "<i>Not set</i>"},
            {"data": "invoice_date", "autoWidth": true, "defaultContent": "<i>Not set</i>"},
            {"data": "due_date", "autoWidth": true, "defaultContent": "<i>Not set</i>"},
            {"data": "amount", "autoWidth": true, "defaultContent": "<i>Not set</i>"},
            {"data": "status", "autoWidth": true, "defaultContent": "<i>Not set</i>"},
            {"data": "created_at", "autoWidth": true, "defaultContent": "<i>Not set</i>"},
            {"data": "", "autoWidth": true, "defaultContent": "<i>Not set</i>"}
        ],
        columnDefs: [
            {
                width: '75px',
                targets: 5,
                orderable: false,
                render: function (data, type, full, meta) {
                    var amount = '₦' + data.toLocaleString();
                    return amount;
                },
            },
            {
                width: '75px',
                targets: 6,
                orderable: false,
                render: function (data, type, full, meta) {
                    let message = ''
                    if (data === 'PENDING') {
                        message = `<span class="badge badge-warning">PENDING</span>`
                    } else if (data === 'DECLINED') {
                        message = `<span class="badge badge-danger">DECLINED</span>`
                    } else {
                        message = `<span class="badge badge-success">APPROVED</span>`
                    }
                    return message;
                },
            },
            {
                targets: -1,
                title: 'Actions',
                orderable: false,
                render: function (data, type, full, meta) {
                    let update_btn = `<button type="button" class="btn btn-primary shadow btn-xs sharp me-1 mr-2 edit" data-id="${full['id']}" data-invoice_number="${full['invoice_number']}"><i class="fas fa-pencil-alt"></i></button>`
                    let delete_btn = `<button type="button" class="btn btn-danger shadow btn-xs sharp delete"><i class="fa fa-trash"></i></button>`
                    return `<div class="d-flex" style="justify-content: space-around">${update_btn}${delete_btn}</div>`;
                },
            }
        ],
    });
    $(".supplier_quotation_tbl tbody").on("click", "tr .edit", function () {
        window.location.replace(`/administrator/quotations-preview/supplier/${$(this).data('id')}`)
        // window.location.href = ''
    });
    $(".filter").on("click", function () {
        if ($(this).data('id') === 'ALL') {
            supplier_quotation_tbl
                .columns(6)
                .search('')
                .draw();
            supplier_quotation_tbl.ajax.reload()
        } else {
            supplier_quotation_tbl
                .columns(6)
                .search($(this).data('id'))
                .draw();
        }
        // window.location.href = ''
    });
    $(".supplier_quotation_tbl tbody").on("click", "tr .delete", function () {
        alert("ddam here")
    });
    let date_range = $('.input-daterange-datepicker')
    date_range.daterangepicker({
        buttonClasses: ['btn', 'btn-sm'],
        applyClass: 'btn-danger',
        cancelClass: 'btn-inverse',
        format: 'DD-MM-YYYY'
    })
    date_range.on('apply.daterangepicker', function (ev, picker) {
        //do something, like clearing an input
        if ($('#filter_by').val() === 'by_invoice_date') {
            supplier_quotation_tbl
                .columns(4)
                .search('')
                .draw();
            supplier_quotation_tbl
                .columns(3)
                .search(picker.startDate.format('YYYY-MM-DD') + "/" + picker.endDate.format('YYYY-MM-DD'))
                .draw();

        } else if ($('#filter_by').val() === 'by_due_date') {
            supplier_quotation_tbl
                .columns(3)
                .search('')
                .draw();
            supplier_quotation_tbl
                .columns(4)
                .search(picker.startDate.format('YYYY-MM-DD') + "/" + picker.endDate.format('YYYY-MM-DD'))
                .draw();
        }
    })
    date_range.on('cancel.daterangepicker', function (ev, picker) {
        //do something, like clearing an input
        supplier_quotation_tbl
            .columns(4)
            .search('')
            .draw();
        supplier_quotation_tbl
            .columns(3)
            .search('')
            .draw();
    })


})