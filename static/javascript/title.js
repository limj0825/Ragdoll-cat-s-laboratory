var OriginTitile = document.title;
var titleTime;
document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        document.title = '你不要我了吗QAQ' + OriginTitile;
        clearTimeout(titleTime);
    }
    else {
        document.title = '(*´∇｀*)你回来啦' + OriginTitile;
        titleTime = setTimeout(function() {
            document.title = OriginTitile;
            }, 2000);
    }
});