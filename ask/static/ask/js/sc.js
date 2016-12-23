window.onload = function () {

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }

            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    });
    $(".plus, .minus").click(function () {
        id = this.id;
        $.ajax({
            url: '/rate',
            dataType: "json",
            method: "POST",
            data: {tp: id},
            success: function (data, textStatus) {
                $('#n' + id.substr(1)).text(data.new)
            }
        })
    })
};