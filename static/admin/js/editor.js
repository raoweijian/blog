$(function(){
    showdown.setOption('simpleLineBreaks', true);
    var converter = new showdown.Converter();

    $('#mdeditor').bind('input', function() {
        var to_html = converter.makeHtml($(this).val());
        $('#preview').html(to_html);
    });
});
