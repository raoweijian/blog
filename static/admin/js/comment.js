$(function(){
    //点击后 展开/折叠 输入框
    $(".comment_button").click(function(){
        var div = $(this).parent().next().toggle();
    });

    //提交评论
    $(".submit-comment").click(function(){
        var user_name = $(this).prev().prev().children("input").val();
        var input = $(this).prev().children("input").val();
        var comment_id = $(this).parent().parent().attr('id');
        var current_url = window.location.href;

        var node = $(this);
        $.ajax({
            url: "/blog/submit_comment/",
            type: 'POST',
            data: {
                content: input,
                comment_id: comment_id,
                user_name: user_name,
                current_url: current_url,
            },
            success: function(ret){
                if (comment_id != null){
                    //先清空输入框
                    node.prev().children('input').val('');
                    node.prev().prev().children('input').val('');
                    node.parent().toggle();

                    new_div = node.parent().parent().clone(true);
                    new_div.attr('id', ret);
                    spans = new_div.children('p').children('span');

                    //console.log(spans[0]);
                    $(spans[0]).html(user_name);
                    var reply_to = node.parent().prev().prev().children(':first').html();
                    $(spans[2]).html(reply_to);
                    $(spans[3]).html(" : " + input + " ");

                    node.parent().parent().parent().append(new_div);
                }else{
                    //清空输入框
                    node.prev().children('input').val('');
                    node.prev().prev().children('input').val('');

                    var panel = create_panel(user_name, input, ret);
                    node.parent().before(panel);
                }
            }
        });
    });
});

function create_panel(user_name, content, comment_id){
    var panel = $('<div class="panel"></div>');
    var comment = $('<div></div>');
    comment.attr('id', comment_id);

    //p1
    var p1 = $('<p></p>');
    var span1 = $('<span class="user_name"></span>');
    span1.html(user_name);
    var span2 = $('<span></span>');
    span2.html(" : " + content + " ");
    p1.append(span1);
    p1.append(span2);

    //p2
    var p2 = $('<p align="right"></p>');
    p2.append($('<a href="javascript:;" class="comment_button">回复</a>'));
    comment.append(p1);
    comment.append(p2);

    panel.append(comment);
    panel.append($('<div style="display: none;"><div class="input-group"><span class="input-group-addon">用户名</span><input type="text" class="form-control"></div><div class="input-group"><span class="input-group-addon">内容</span><input type="text" class="form-control"></div><button class="btn btn-default submit-comment" type="button">提交</button></div>'));
    return panel;
}
