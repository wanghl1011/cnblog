$(document).ready(function () {
    var parent_comment_id = "";
    var $ul = $("ul.list-group");
    var $textarea = $("#comment_content");
    // 提交评论按钮
    $('#sub_comment').on("click", function () {
        var username = $(".msg").attr("user");
        var path = $(".msg").attr("path");
        if (username) {
            var textval = $textarea.val();
            if (parent_comment_id) {
                // console.log($textarea.val());
                var length1 = $(this).attr("pcom_username").length + 1;
                // console.log(length1);
                // console.log(textval.trim().indexOf("\n")) ;
                var warnning = "别瞎几把改";
                if (textval.trim().charAt(0) !== "@") {
                    // console.log(1);
                    alert(warnning);
                    parent_comment_id = "";
                    $textarea.val("");
                    return false
                }
                else if (textval.trim().indexOf("\n") !== length1) {
                    // console.log(2);
                    alert(warnning);
                    $textarea.val("");
                    parent_comment_id = "";
                    return false
                }
                else if (textval.trim().match("\n\n")) {
                    // console.log(3);
                    alert(warnning);
                    $textarea.val("");
                    parent_comment_id = "";
                    return false
                }
            }
            $.ajax({
                url: "/blog/comment",
                type: 'post',
                data: {
                    article_id: $('#article_id').attr("article_id"),
                    content: textval,
                    parent_comment_id: parent_comment_id,
                    csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val()
                },
                success: function (data) {
                    if (data.sta === 1) {
                        // console.log(data);
                        var $li = $("li.li");
                        var num = $li.length + 1;
                        var a1 = "<a href='/blog/" + data.rusername + "'>";
                        var a2 = "<a style='margin-right: 10px' role='button' class='reply' username='" + data.rusername + "' comment_id='" + data.nid + "'>回复</a>";
                        // 子评论
                        if (data.parent_comment_user) {
                            var a3 = '<a href="/blog/' + data.parent_comment_user + '">' + data.parent_comment_user + '</a>';
                            var info = '<div class="well"><span>@' + a3 + '</span>&nbsp;&nbsp;<span>' + data.parent_comment_content + '</span></div>';
                            var leaf_comment_info = "<li class='list-group-item li'><div><span>#" + num + "楼</span><span class='span'>" + data.ctime + "</span><span class='span'>" + a1 + data.rusername + "</a></span><span class='pull-right'>" + a2 + "</span></div>" + info + "<div>" + data.com_content + "</div></li>";
                            $ul.append(leaf_comment_info);
                        }
                        // 根评论
                        else {
                            // console.log($li);
                            var root_comment_info = "<li class='list-group-item li'><div><span>#" + num + "楼</span><span class='span'>" + data.ctime + "</span><span class='span'>" + a1 + data.rusername + "</a></span><span class='pull-right'>" + a2 + "</span></div><div>" + data.com_content + "</div></li>";
                            // console.log(comment_info);
                            $("li.empty").remove();
                            $ul.append(root_comment_info);
                        }
                        // 清空评论内容
                        $("#comment_content").val("");
                        //清空父评论的id
                        parent_comment_id = "";
                        //清空提交按钮自定义属性
                        $("#sub_comment").removeAttr("pcom_username")

                    } else {
                        alert(data.msg);
                        location.href = "/blog/login_confirm";
                    }

                }
            })
        } else {
            location.href = "/blog/login_confirm?next=" + path;
        }

    });

    // 回复评论按钮
    $(".list-group").on("click", ".reply", function () {
        var username = $(".msg").attr("user");
        var path = $(".msg").attr("path");
        if (username) {

        } else {
            location.href = "/blog/login_confirm?next=" + path;
            return false
        }
        var $com_user = $(this).attr("username");
        var $com_id = $(this).attr("comment_id");
        var info = "@" + $com_user + "\n";
        $("#sub_comment").attr({"pcom_username": $com_user});
        parent_comment_id = $com_id;
        $textarea.val(info);
        $textarea.focus();
    });

    // $textarea.blur(function () {
    //     $textarea.val("");
    // })
    var article_id = $("#article_id").attr("article_id");
    $.ajax({
        url: "/blog/get/comment/tree/" + article_id,
        success: function (data) {
            // console.log(data);
            var info = show_comment_tree(data);
            console.log(info);
            $(".comment_tree").append(info);
            // $(".comment").css({"border":"1px solid gray"});
            // $(".comment .comment").css({"margin-left":"20px"});
            $("li li").css({"margin-left": "20px"});
            $(".comment-img").css({"width": "40px", "height": "40px"})
        }
    });

    function show_comment_tree(comment_tree) {
        var htmls = "";
        $.each(comment_tree, function (k, comment) {
            console.log(comment["content"]);
            var content = '<ul class="list-group"><li class="list-group-item"><div class="comment"><div class="content"><div><span><img class="comment-img" src="' + comment["avatar"] + '" alt="">&nbsp;&nbsp;</span><span>' + comment["ctime"] + '</span>&nbsp;&nbsp;<span><a href="/blog/' + comment["user"] + '">' + comment["user"] + '</a></span></div><div style="margin-left: 48px">' + comment["content"] + '</div></div>';
            // 有子评论
            if (comment["child_list"]) {
                // var content1='<div class="comment" style="margin-left: 50px"><div class="content"><span>';
                content += show_comment_tree(comment["child_list"]);
            }
            content += '</div></li></ul>';
            htmls += content;
        });
        return htmls
    }


    // 删除评论按钮
    // $(".delete_comment").on("click",function () {
    //     var com_id=$(this).attr("comment_id");
    //     var article_id=$("#article_id").attr("article_id");
    //     console.log(com_id,article_id);
    //     $.ajax({
    //         url:'/blog/del/comment',
    //         type:'post',
    //         data:{
    //             comment_id:com_id,
    //             article_id:article_id,
    //             csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val()
    //         },
    //         success:function (data) {
    //             console.log(data);
    //             if (data.sta===1){
    //                 $(this).parent().parent().parent().remove();
    //             }
    //             else{
    //                 alert(data.msg)
    //             }
    //         }
    //     })
    // })
});