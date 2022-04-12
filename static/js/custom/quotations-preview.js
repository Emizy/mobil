$(document).ready(function () {
    getSupplierCopy($('#identifier').val())
    getStationCopy($('#identifier').val())
    $('#accept_quotation').on('click', function (event) {

        swal({
            title: "Are you sure to accept ?",
            text: "Clicking accept, A notification will be sent to the supplier pertaining to this approval",
            type: "info",
            showCancelButton: !0,
            confirmButtonColor: "#56f584",
            confirmButtonText: "Yes, accept it !!",
            cancelButtonText: "No, close it !!",
            closeOnConfirm: !1,
            closeOnCancel: !1
        }).then((function (t) {
            if (t.value) {
                swal.fire({
                    title: 'Processing request',
                    allowEscapeKey: false,
                    allowOutsideClick: false,
                    onOpen: () => {
                        swal.showLoading();
                    }
                })
                let formdata = new FormData()
                formdata.append('invoice_number', $('#invoice_number').val());
                formdata.append('status', 'APPROVED');
                axios.post(`/administrator/quotations-preview/supplier/${$('#invoice_number').val()}`, formdata, {headers: {'X-CSRFTOKEN': $('input[name=csrfmiddlewaretoken]').val(),}})
                    .then(response => {
                        Swal.close()
                        getSupplierCopy($('#identifier').val())
                        getStationCopy($('#identifier').val())
                        swal("Success !!", "Quotation marked as approved successfully", "success")
                    })
                    .catch(error => {
                        Swal.close()
                        if (error.response.status === 400) {
                            swal("info", error.response.data.message, "info")
                        } else {
                            swal("info", "Ops,Something went wrong while processing your request,Kindly Try Again", "warning")
                        }
                    })
            }
        }))
    })
    $('#decline_quotation').on('click', function (event) {

        swal({
            title: "Are you sure to decline ?",
            text: "Clicking decline, A notification will be sent to the supplier pertaining to this quotation decline",
            type: "warning",
            showCancelButton: !0,
            confirmButtonColor: "#e23428",
            confirmButtonText: "Yes, decline it !!",
            cancelButtonText: "No, close it !!",
            closeOnConfirm: !1,
            closeOnCancel: !1
        }).then((function (t) {
            console.log(t)
            if (t.value) {
                swal.fire({
                    title: 'Processing request',
                    allowEscapeKey: false,
                    allowOutsideClick: false,
                    onOpen: () => {
                        swal.showLoading();
                    }
                })
                let formdata = new FormData()
                formdata.append('invoice_number', $('#invoice_number').val());
                formdata.append('status', 'DECLINED');
                axios.post(`/administrator/quotations-preview/supplier/${$('#invoice_number').val()}`, formdata, {headers: {'X-CSRFTOKEN': $('input[name=csrfmiddlewaretoken]').val(),}})
                    .then(response => {
                        Swal.close()
                        getSupplierCopy($('#identifier').val())
                        getStationCopy($('#identifier').val())
                        swal("Success !!", "Quotation marked as declined successfully", "success")
                    })
                    .catch(error => {
                        Swal.close()
                        if (error.response.status === 400) {
                            swal("info", error.response.data.message, "info")
                        } else {
                            swal("info", "Ops,Something went wrong while processing your request,Kindly Try Again", "warning")
                        }
                    })
            }
        }))
    })
})

function getSupplierCopy(id) {
    axios.get(`/administrator/quotations-copy/?type=supplier&id=${id}`, {headers: {'X-CSRFTOKEN': $('input[name=csrfmiddlewaretoken]').val(),}}).then(function (response) {
        $('#supplier-copy').html(response.data.template)
    }).catch(function (error) {


    });

}

function getStationCopy(id) {
    axios.get(`/administrator/quotations-copy/?type=station&id=${id}`, {headers: {'X-CSRFTOKEN': $('input[name=csrfmiddlewaretoken]').val(),}}).then(function (response) {
        $('#station-copy').html(response.data.template)
    }).catch(function (error) {


    });

}