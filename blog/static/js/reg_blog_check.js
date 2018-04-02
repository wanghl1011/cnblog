$(document).ready(function () {
    $("#check_img").on("click", function () {
        console.log("ok");
        $("#check_img")[0].src += "?";
    });
    $("#file").on("change", function () {
        var file_img = $("#file")[0].files[0];
        var reader = new FileReader();
        reader.readAsDataURL(file_img);
        reader.onload = function () {
            $("img.img").attr("src", reader.result)
        };
    });
    $(".sub").on("click", function () {
        console.log("ok");
        var $formdata = new FormData();
        var file_img = $("#file")[0].files[0];
        $formdata.append("username", $("#id_username").val());
        $formdata.append("password", $("#id_password").val());
        $formdata.append("repassword", $("#id_repassword").val());
        $formdata.append("email", $("#id_email").val());
        $formdata.append("file", file_img);
        $formdata.append("check_code", $("#id_check_code").val());
        $formdata.append("csrfmiddlewaretoken", $("[name=csrfmiddlewaretoken]").val());
        $.ajax({
            url: "/blog/reg_check/",
            type: 'post',
            data: $formdata,
            contentType: false,
            processData: false,
            success: function (data) {
                $(".error").text("").removeClass("pull-right").parent().removeClass("has-error");
                if (data.sta === 1) {
                    location.href = "/blog/index/";
                } else {
                    var error_data = data.msg;
                    $.each(error_data, function (i, j) {
                        if (i!=="__all__"){
                            $("#id_" + i).next().text(j[0]).addClass("pull-right").parent().addClass("has-error")
                        }
                        else{
                            $("#id_repassword").next().text(j[0]).addClass("pull-right").parent().addClass("has-error")
                        }
                    })
                }
            }
        })
    });
    // var handlerPopup = function (captchaObj) {
    //     // 成功的回调
    //     captchaObj.onSuccess(function () {
    //         var validate = captchaObj.getValidate();
    //         $.ajax({
    //             url: "/blog/pc-geetest/ajax_validate", // 进行二次验证
    //             type: "post",
    //             dataType: "json",
    //             data: {
    //                 username: $('#username1').val(),
    //                 password: $('#password1').val(),
    //                 csrfmiddlewaretoken:$("[name=csrfmiddlewaretoken]").val(),
    //                 geetest_challenge: validate.geetest_challenge,
    //                 geetest_validate: validate.geetest_validate,
    //                 geetest_seccode: validate.geetest_seccode
    //             },
    //             success: function (data) {
    //                 if (data && (data.status === "success")) {
    //                         var $formdata = new FormData();
    //                         var file_img = $("#file")[0].files[0];
    //                         $formdata.append("username", $("#id_username").val());
    //                         $formdata.append("password", $("#id_password").val());
    //                         $formdata.append("repassword", $("#id_repassword").val());
    //                         $formdata.append("email", $("#id_email").val());
    //                         $formdata.append("file", file_img);
    //                         $formdata.append("check_code", $("#id_check_code").val());
    //                         $formdata.append("csrfmiddlewaretoken", $("[name=csrfmiddlewaretoken]").val());
    //                         console.log("ok");
    //                         $.ajax({
    //                             url: "/blog/reg_check/",
    //                             type: 'post',
    //                             data: $formdata,
    //                             contentType: false,
    //                             processData: false,
    //                             success: function (data) {
    //                                 $(".error").text("").removeClass("pull-right").parent().removeClass("has-error");
    //                                 if (data.sta === 1) {
    //                                     console.log("++++++++++++++++++++++");
    //                                     location.href = "/blog/login_confirm/"
    //                                 } else {
    //                                     var error_data = data.msg;
    //                                     $.each(error_data, function (i, j) {
    //                                         if (i!=="__all__"){
    //                                             $("#id_" + i).next().text(j[0]).addClass("pull-right").parent().addClass("has-error")
    //                                         }
    //                                         else{
    //                                             $("#id_repassword").next().text(j[0]).addClass("pull-right").parent().addClass("has-error")
    //                                         }
    //                                     })
    //                                 }
    //                             }
    //                         })
    //                 } else {
    //                     location.reload()
    //                 }
    //             }
    //         });
    //     });
    //     $("#popup-submit").click(function () {
    //         captchaObj.show();
    //     });
    //     // 将验证码加到id为captcha的元素里
    //     captchaObj.appendTo("#popup-captcha");
    //     // 更多接口参考：http://www.geetest.com/install/sections/idx-client-sdk.html
    // };
    // 验证开始需要向网站主后台获取id，challenge，success（是否启用failback）
    // $.ajax({
    //     url: "/blog/pc-geetest/register?t=" + (new Date()).getTime(), // 加随机数防止缓存
    //     type: "get",
    //     dataType: "json",
    //     success: function (data) {
    //         // 使用initGeetest接口
    //         // 参数1：配置参数
    //         // 参数2：回调，回调的第一个参数验证码对象，之后可以使用它做appendTo之类的事件
    //         initGeetest({
    //             gt: data.gt,
    //             challenge: data.challenge,
    //             product: "popup", // 产品形式，包括：float，embed，popup。注意只对PC版验证码有效
    //             offline: !data.success // 表示用户后台检测极验服务器是否宕机，一般不需要关注
    //             // 更多配置参数请参见：http://www.geetest.com/install/sections/idx-client-sdk.html#config
    //         }, handlerPopup);
    //     }
    // });
});