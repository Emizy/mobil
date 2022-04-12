$(document).ready(function () {
    $('#login-form').on('submit', function (e) {
        e.preventDefault()
        var data = {
            'username': $('#username').val(),
            'password': $('#password').val()
        }
        let btn = $('#lab_btn')
        btn.attr('disabled')
        btn.html('Loading <i class="fa fa-spinner fa-spin"></i>')
        for (const [key, value] of Object.entries(data)) {
            if (value === '' || value === null) {
                btn.html('Sign Me In')
                btn.removeAttr('disabled');
                toastr.warning("All field are required", {
                    closeButton: !0,
                    tapToDismiss: !1
                })
                return false
            }
        }
        axios.post('/login/', data, {headers: {'X-CSRFTOKEN': $('input[name=csrfmiddlewaretoken]').val(),}}).then(function (response) {
            btn.removeAttr('disabled');
            btn.html('Sign Me In')
            var resp = response.data;
            toastr.success("Login Successful", {
                closeButton: !0,
                tapToDismiss: !1
            })
            window.location.replace(resp.url);
        }).catch(function (error) {
            btn.removeAttr('disabled')
            btn.removeClass('running');
            btn.html('Sign Me In')
            toastr.warning(error.response.data.message, {
                closeButton: !0,
                tapToDismiss: !1
            })

        });

    })
    $('#accept-form').on('submit', function (e) {
        e.preventDefault()
        var data = {
            'type': $('#type').val(),
            'token': $('#token').val(),
            'address': $('#address').val(),
            'password': $('#password').val(),
        }
        let btn = $('#sub_btn')
        btn.attr('disabled')
        btn.html('Loading <i class="fa fa-spinner fa-spin"></i>')
        for (const [key, value] of Object.entries(data)) {
            if (value === '' || value === null) {
                btn.html('Accept  invitation')
                btn.removeAttr('disabled');
                toastr.warning("All field are required", {
                    closeButton: !0,
                    tapToDismiss: !1
                })
                return false
            }
        }
        if (data.password !== $('#confirm_password').val()) {
            btn.html('Accept  invitation')
            btn.removeAttr('disabled');
            toastr.warning("Password does not match", {
                closeButton: !0,
                tapToDismiss: !1
            })
            return false
        }
        axios.post(`/accept/${$('#type').val()}/${$('#token').val()}/`, data, {headers: {'X-CSRFTOKEN': $('input[name=csrfmiddlewaretoken]').val(),}}).then(function (response) {
            btn.removeAttr('disabled');
            btn.html('Accept  invitation')
            var resp = response.data;
            toastr.success("Invitation sent successfully", {
                closeButton: !0,
                tapToDismiss: !1
            })
            window.location.replace('/login');
        }).catch(function (error) {
            btn.removeAttr('disabled')
            btn.removeClass('running');
            btn.html('Accept  invitation')
            toastr.warning(error.response.data.message, {
                closeButton: !0,
                tapToDismiss: !1
            })

        });

    })
})