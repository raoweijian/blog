/*
    showdown.setOption('simpleLineBreaks', true);
    var converter = new showdown.Converter();

    //页面加载完，马上进行一次转换
    var to_html = converter.makeHtml($('#mdeditor').val());
    $('#preview').html(to_html);

    // mdeditor 变化时，进行转换
    $('#mdeditor').on('input', function() {
        var to_html = converter.makeHtml($(this).val());
        $('#preview').html(to_html);
        $('pre code').each(function(i, block){
            hljs.highlightBlock(block);
        });
    });

    $('textarea').pastableTextarea();

    //粘贴截图
    $('#mdeditor').on('pasteImage', function (ev, data){
        $.ajax({
            url: "/upload_picture/",
            type: 'POST',
            data: {
                abc: data.dataURL,
            },
            success: function(ret){
                var new_html = $('#mdeditor').val() + "![图片](" + ret + ")\n";

                $('#mdeditor').val(new_html);

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
        //console.log("text: " + data.text);
    });

    //提交
    $("#button_publish").on({
        click: function(){
            $.post(
                "/publish/",
                {
                    content: $('#mdeditor').val(),
                    title: $('#title').val(),
                },
                function(data){
                    window.location.href = data;
                },
            );
        },
    })

    //同步滚动
    $("textarea#mdeditor").on('scroll', function(){
        $preview = $("div#preview");
        var percentage = this.scrollTop / (this.scrollHeight - this.offsetHeight);
        var height = percentage * ($preview.get(0).scrollHeight - $preview.get(0).offsetHeight);
        $preview.scrollTop(height);
    });

    indent(document.getElementById("mdeditor"));

    function indent(tx){
        tx.addEventListener("keydown", function(event){
            if(event.keyCode === 13){
                event.preventDefault();
                insert("\n");
            }

            if(event.keyCode === 9){
                var position = this.selectionStart + 4;
                this.value = this.value.substr(0, this.selectionStart) + '    ' + this.value.substr(this.selectionStart);
                this.selectionStart = position;
                this.selectionEnd = position;
                this.focus();
                event.preventDefault();
            }

        });

        function insert(v){
            var txt = tx.value;
            var point = tx.selectionEnd; //当前光标所在位置
            console.log("point: " + point);

            var sn = txt.lastIndexOf('\n', point - 1); //当前光标所在行的前一个换行符所在位置
            console.log("sn: " + sn);
            var x1 = txt.substring(sn + 1, txt.length); //当前光标所在行，光标之前的字符串

            //匹配行首的空格，这里用 [ *] 而不是 [\s*] ，是因为如果当前行全是空格，那么 \s* 会匹配到下一个换行符，导致最终多插入了一个换行符
            var reg = /^ * /gi
            spaces = x1.match(reg)[0];
            left = txt.substring(0, point);
            right = txt.substring(point, txt.length);
            console.log("x1: [" + x1 + "]")
            console.log("spaces: [" + spaces + "]");

            txt = left  + v + spaces + right;

            tx.value = txt;
            tx.setSelectionRange(point + spaces.length + 1, point + spaces.length + 1)
        }
    }
*/

'use strict';
Vue.use(window.vuelidate.default);
const { required, minLength } = window.validators;

$(function(){
    showdown.setOption('simpleLineBreaks', true);
    $('textarea').pastableTextarea();

    let app = new Vue({
        el: '#container',
        data: {
            content: '',
            title: '',
            converter: new showdown.Converter(),
        },

        computed: {
            mdContent: function(){
                return this.converter.makeHtml(this.content);
            },
        },

        //初始化，获取全文内容
        mounted: function(){
            //获取标题
            let uriList = location.href.split("/");
            if(uriList.pop() == "edit"){
                this.title = decodeURI(uriList.pop());
                axios.get('/api/article/?title=' + this.title)
                .then((response) => {
                        this.content = response.data[0].content;
                })
                .catch((error) => {
                    console.log(error);
                });
            }
        },

        updated: function(){
            $('pre code').each(function(i, block){
                hljs.highlightBlock(block);
            });
        },

        methods: {
            update: function(e){
                this.content = e.target.value;
            },

            //粘贴截图
            pasteImage: async function(e){
                let clipboardData = e.clipboardData;

                if(clipboardData){
                    let items = clipboardData.items;
                    let types = clipboardData.types || [];
                    if(!items){
                        console.log(2)
                        return;
                    }

                    let item = items[0];
                    for(let i = 0; i < types.length; i++ ){
                        if(types[i] === 'Files'){
                            item = items[i];
                            break;
                        }
                    }
                    if(item && item.kind === 'file' && item.type.match(/^image\//i)){
                        let reader = imgReader(item);
                        await sleep(50);
                        $.ajax({
                            url: "/upload_picture/",
                            type: 'POST',
                            data: {
                                abc: reader.result,
                            },
                            success: ((ret) => {
                                this.content = this.content + "![图片](" + ret + ")\n";
                            }),
                        });
                    }
                }
            },

            //同步滚动
            syncScroll: function(e){
                let percentage = e.target.scrollTop / (e.target.scrollHeight - e.target.offsetHeight);
                let $preview = $("#preview");
                let height = percentage * ($preview.get(0).scrollHeight - $preview.get(0).offsetHeight);
                $preview.scrollTop(height);
            },

            //发布
            publish: function(){
                if(this.title.length == 0){
                    alert("标题不能为空");
                    return;
                }
                axios.post('/publish/', {
                    content: this.content,
                    title: this.title,
                },
                {
                    transformRequest: [function (data) {
                        let ret = new URLSearchParams();
                        for (let it in data) {
                            ret.append(it, data[it]);
                        }
                        return ret;
                    }],
                })
                .then(function (response){
                    window.location.href = response.data;
                })
                .catch(function (error) {
                    console.log(error);
                });
            },

            //监听 tab 和回车键
            enter: async function(e){
                e.preventDefault();
                let txt = e.target.value;
                let point = e.target.selectionEnd;

                let sn = txt.lastIndexOf('\n', point - 1);
                let x1 = txt.substring(sn + 1, txt.length);
                let reg = /^ */gi;
                let spaces = x1.match(reg)[0];
                let left = txt.substring(0, point);
                let right = txt.substring(point, txt.length);

                this.content = left  + "\n" + spaces + right;
                await sleep(10);
                e.target.setSelectionRange(point + spaces.length + 1, point + spaces.length + 1);
            },
            tab: async function(e){
                e.preventDefault();
                let $el = e.target;
                let position = $el.selectionStart + 4;
                this.content = $el.value.substr(0, $el.selectionStart) + '    ' + $el.value.substr($el.selectionStart);
                await sleep(10);

                $el.selectionStart = position;
                $el.selectionEnd = position;
                $el.focus();
            },
        },

        validations: {
            title: {
                required,
                minLength: minLength(5)
            }
        }
    });
});
