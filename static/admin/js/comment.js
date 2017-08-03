function expand_comment_input(button){
    var clicked = button.getAttribute("clicked");
    if (clicked == "no"){
        var div = button.parentNode.parentNode;
        comment_id = div.getAttribute("id");

        //创建一个div
        var input_div = document.createElement('div');
        input_div.setAttribute('id', "input");

        //div里创建一个输入框
        var input = document.createElement('input');
        input.setAttribute('type', 'text');
        input.setAttribute('class', 'form-control');

        //塞进去
        input_div.appendChild(input);
        div.appendChild(input_div);

        //修改clicked状态
        button.setAttribute("clicked", "yes");
    }else if (clicked == "yes"){
        $(button.parentNode.parentNode).children('#input').hide();
        button.setAttribute("clicked", "closed");
    }else if (clicked == "closed"){
        $(button.parentNode.parentNode).children('#input').show();
        button.setAttribute("clicked", "yes");
    }
}
