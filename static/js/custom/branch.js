$(document).ready(function () {
    $('#create-branch').on('submit', function (event) {
        event.stopImmediatePropagation()
        event.preventDefault()
        let formdata = new FormData(this)
        let btn = $('#sub-btn')
        btn.attr('disabled')
        btn.html('Loading <i class="fa fa-spinner fa-spin"></i>')
        for (const [key, value] of Object.entries(formdata)) {
            if (value === '' || value === null) {
                btn.html('Submit')
                btn.removeAttr('disabled');
                swal({
                    title: "Notification",
                    text: "All field are required",
                    showConfirmButton: true,
                    type: 'warning'
                })
                return false
            }
        }
        axios.post('/supplier/create-branch/', formdata, {headers: {'X-CSRFTOKEN': $('input[name=csrfmiddlewaretoken]').val(),}}).then(function (response) {
            btn.removeAttr('disabled');
            btn.html('Submit')
            swal({
                title: "Success",
                text: "Quotation entry submitted successfully",
                showConfirmButton: true,
                type: 'success'
            })
            setTimeout(function () {
                window.location.replace('/supplier/branch/');
            }, 2000)
        }).catch(function (error) {
            btn.removeAttr('disabled')
            btn.removeClass('running');
            btn.html('Submit')
            swal({
                title: "ERROR",
                text: error.response.data.message,
                showConfirmButton: true,
                type: 'warning'
            })

        });

    })
    let branch_tbl = $("#branch_tbl").DataTable({
        "dom": '<"top"Brt><"bottom"ip><"clear">',
        "processing": true,
        "serverSide": true,
        lengthChange: !1,
        responsive: true,
        "pageLength": 100,
        "searching": true,
        "paging": true,
        ajax: {
            "url": '/supplier/branch/',
            'type': 'POST',
            'data': {
                'csrfmiddlewaretoken': $("[name=csrfmiddlewaretoken]").val(),
                columnsDef: [
                    'name', 'state', 'created_at', ''],
            }
        },
        columns: [
            {"data": "name", "autoWidth": true, "defaultContent": "<i>Not set</i>"},
            {"data": "state", "autoWidth": true, "defaultContent": "<i>Not set</i>"},
            {"data": "created_at", "autoWidth": true, "defaultContent": "<i>Not set</i>"},
            {"data": "", "autoWidth": true, "defaultContent": "<i>Not set</i>"}
        ],
        columnDefs: [
            {
                targets: -1,
                title: 'Actions',
                orderable: false,
                render: function (data, type, full, meta) {
                    let update_btn = `<button type="button" class="btn btn-secondary btn-xxs shadow me-1 mr-2 edit" data-id="${full['id']}">Add user</button>`
                    let delete_btn = `<button type="button" class="btn btn-danger btn-xxs shadow delete">Delete</button>`
                    return `<div class="d-flex">${update_btn}${delete_btn}</div>`;
                    return '';
                },
            }
        ],
    });


})