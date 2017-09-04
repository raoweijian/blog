$(function(){
    showdown.setOption('simpleLineBreaks', true);
    var converter = new showdown.Converter();

    //页面加载完，马上进行一次转换
    var to_html = converter.makeHtml($('#mdeditor').val());
    $('#preview').html(to_html);

    // mdeditor 变化时，进行转换
    $('#mdeditor').bind('input', function() {
        var to_html = converter.makeHtml($(this).val());
        $('#preview').html(to_html);
    });

    $('textarea').pastableTextarea();

    //粘贴截图
    $('#mdeditor').on('pasteImage', function (ev, data){
        $.ajax({
            url: "/blog/upload_picture/",
            type: 'POST',
            data: {
                abc: data.dataURL,
            },
            success: function(ret){
                console.log(ret);
                var new_html = $('#mdeditor').val() + "![图片](" + ret + ")\n";
                console.log("new_html is " + new_html);

                $('#mdeditor').val(new_html);
                console.log("new mdeditor is " + $('#mdeditor').val());

                //手动更新一下预览区
                var to_html = converter.makeHtml($('#mdeditor').val());
                $('#preview').html(to_html);
            },
        });
    }).on('pasteImageError', function(ev, data){
        alert('Oops: ' + data.message);
        if(data.url){
            alert('But we got its url anyway:' + data.url)
        }
    }).on('pasteText', function (ev, data){
        console.log("text: " + data.text);
    });

    //提交
    $("#button_publish").on({
        click: function(){
            $.post(
                "/blog/publish/",
                {
                    content: $('#mdeditor').val(),
                    title: $('#title').val(),
                },
                function(data){
                    console.log(data);
                    window.location.href = data;
                },
            );
        },
    })
});
