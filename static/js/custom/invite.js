$(document).ready(function () {
    $('#submit-form').on('submit', function (e) {
        e.preventDefault()
        var data = {
            'name': $('#name').val(),
            'email': $('#email').val(),
            'type': $('#type').val(),
        }
        let btn = $('#sub-btn')
        btn.attr('disabled')
        btn.html('Loading <i class="fa fa-spinner fa-spin"></i>')
        for (const [key, value] of Object.entries(data)) {
            if (value === '' || value === null) {
                btn.html('Send invite')
                btn.removeAttr('disabled');
                toastr.warning("All field are required", {
                    closeButton: !0,
                    tapToDismiss: !1
                })
                return false
            }
        }
        axios.post('/administrator/invitation/create/', data, {headers: {'X-CSRFTOKEN': $('input[name=csrfmiddlewaretoken]').val(),}}).then(function (response) {
            btn.removeAttr('disabled');
            btn.html('Send invite')
            var resp = response.data;
            toastr.success("Invitation sent successfully", {
                closeButton: !0,
                tapToDismiss: !1
            })
            window.location.replace(resp.url);
        }).catch(function (error) {
            btn.removeAttr('disabled')
            btn.removeClass('running');
            btn.html('Send invite')
            toastr.warning(error.response.data.message, {
                closeButton: !0,
                tapToDismiss: !1
            })

        });

    })

})