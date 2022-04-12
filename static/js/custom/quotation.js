$(document).ready(function () {

    let invoice_date = $('#invoice_date')
    invoice_date.bootstrapMaterialDatePicker({
        time: false
    }).on('change', function (e, date) {
        let due_date = moment(date.format('YYYY-MM-DD')).add(30, 'days')
        $('#due_date').val(due_date.format('YYYY-MM-DD'))
    });

    $('#supplier-quotation').on('submit', function (event) {
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
        axios.post('/supplier/create-quotation/', formdata, {headers: {'X-CSRFTOKEN': $('input[name=csrfmiddlewaretoken]').val(),}}).then(function (response) {
            btn.removeAttr('disabled');
            btn.html('Submit')
            var resp = response.data;
            swal({
                title: "Success",
                text: "Quotation entry submitted successfully",
                showConfirmButton: true,
                type: 'success'
            })
            window.location.replace('/supplier/quotation/');
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


})