$(document).ready(function () {
    $("#check_img").on("click", function () {
        $("#check_img")[0].src += "?";
    });
    // $("#submit").on("click",function () {
    //     $.ajax({
    //         url:"/blog/login_confirm/",
    //         type:"post",
    //         data:{
    //             username:$("#username").val(),
    //             password:$("#password").val(),
    //             check_code:$("#check_code").val(),
    //             csrfmiddlewaretoken:$("[name=csrfmiddlewaretoken]").val()
    //         },
    //         success:function (data) {
    //             if (data.sta===1){
    //                 if (location.search.slice(6)){
    //                     var lujing=location.search.slice(6);
    //                     location.href=lujing;
    //                 }else{
    //                     location.href="/blog/index/";
    //                 }
    //
    //             }
    //             else{
    //                 $(".error").text(data.msg)
    //             }
    //         }
    //     })
    //
    // });
    // setTimeout(function () {
    //   $(".error").text("")
    // },3000);


    // $("#popup-submit").on("click", function () {
        var handlerPopup = function (captchaObj) {
            // 成功的回调
            captchaObj.onSuccess(function () {
                var validate = captchaObj.getValidate();
                $.ajax({
                    url: "/blog/pc-geetest/ajax_validate", // 进行二次验证
                    type: "post",
                    dataType: "json",
                    data: {
                        username: $("#username").val(),
                        password: $("#password").val(),
                        csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
                        geetest_challenge: validate.geetest_challenge,
                        geetest_validate: validate.geetest_validate,
                        geetest_seccode: validate.geetest_seccode
                    },
                    success: function (data) {
                        if (data.sta === 1) {
                            if (location.search.slice(6)) {

                                location.href = location.search.slice(6);
                            } else {
                                location.href = "/blog/index/";
                            }

                        }
                        else {
                            $(".error").text(data.msg)
                        }
                    }
                });
            });
            $("#popup-submit").click(function () {
                captchaObj.show();
            });
            // 将验证码加到id为captcha的元素里
            captchaObj.appendTo("#popup-captcha");
            // 更多接口参考：http://www.geetest.com/install/sections/idx-client-sdk.html
        };
        // 验证开始需要向网站主后台获取id，challenge，success（是否启用failback）
        $.ajax({
            url: "/blog/pc-geetest/register?t=" + (new Date()).getTime(), // 加随机数防止缓存
            type: "get",
            dataType: "json",
            success: function (data) {
                // 使用initGeetest接口
                // 参数1：配置参数
                // 参数2：回调，回调的第一个参数验证码对象，之后可以使用它做appendTo之类的事件
                initGeetest({
                    gt: data.gt,
                    challenge: data.challenge,
                    product: "popup", // 产品形式，包括：float，embed，popup。注意只对PC版验证码有效
                    offline: !data.success // 表示用户后台检测极验服务器是否宕机，一般不需要关注
                    // 更多配置参数请参见：http://www.geetest.com/install/sections/idx-client-sdk.html#config
                }, handlerPopup);
            }
        });
    // })
});