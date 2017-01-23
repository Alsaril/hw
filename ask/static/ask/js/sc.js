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
    });
    var modal = document.getElementById('myModal');

    var btn = document.getElementById("ask");

    var span = document.getElementsByClassName("close")[0];

    btn.onclick = function () {
        modal.style.display = "block";
    };


    span.onclick = function () {
        modal.style.display = "none";
    };

    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    };


    function validateForm() {
        $('.text-error').remove();
        var a_title = false;
        var a_image = false;
        var c_category = false;
        var a_text = false;
        var c_video = false;
        var c_date = false;

        var el_t = $('#id_title');
        if (el_t.val().length > 100) {
            a_title = true;
            $('#id_title').after('<span class="text-error">Название должно быть меньше 100 символов</span>');
        }
        if (el_t.val().length == 0) {
            a_title = true;
            $('#id_title').after('<span class="text-error">Поле не может быть пустым</span>');
        }

        if ($('form input[type=file]').val().length == 0) {
            a_image = true;
            $('#id_picture').after('<span class="text-error">Выберите файл</span>');
        }

        var el_tex = $('#id_text');
        if (el_tex.val().length == 0) {
            a_text = true;
            $('#id_text').after('<span class="text-error">Поле не может быть пустым</span>');
        }


        return (a_title || a_image || a_text);
    }

    $('.form_question').on('submit', function (event) {
        if (validateForm()) {
            event.preventDefault();
        }
    });
};