$(document).ready(function () {
    var $up = $("#digg_count");
    var $down = $("#bury_count");
    var $tip = $("#digg_tips");
    $(".up_down").on("click", function () {
        var username = $(".msg").attr("user");
        var path = $(".msg").attr("path");
        if (username) {
            $.ajax({
            url: '/blog/updown/',
            type: 'post',
            data: {
                is_up: $(this).attr("up_down"),
                article_id: $('#article_id').attr("article_id"),
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val()
            },
            success: function (data) {
                if (data.sta === 1) {
                    if (data.is_up === 'up') {
                        var old_up = $up.text();
                        $up.text(parseInt(old_up) + 1)
                    } else {
                        var old_down = $down.text();
                        $down.text(parseInt(old_down) + 1)
                    }
                } else {
                    $tip.text(data.msg)
                }
            }
        });
        setTimeout(function () {
            $tip.text("")
        }, 3000)
        } else {
            location.href = "/blog/login_confirm?next=" + path;
        }

    })
});