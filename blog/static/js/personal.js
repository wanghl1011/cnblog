$("#manage").on("click",function () {
        var username=$(".info").attr("user");
        var path=$(".info").attr("path");
        if (username.length>0){
            console.log("ok");
            location.href='/blog/manage/'+username;
        }else{
            console.log("nook");
            location.href="/blog/login_confirm?next="+path;
        }
    });