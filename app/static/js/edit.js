$(function(){
    showdown.setOption('simpleLineBreaks', true);
    $('textarea').pastableTextarea();

    let app = new Vue({
        el: '#container',
        data: {
            content: '',
            title: '',
            converter: new showdown.Converter(),
            id: "",
        },

        computed: {
            mdContent: function(){
                return this.converter.makeHtml(this.content);
            },
        },

        //初始化，获取全文内容
        mounted: function(){
            this.getId();
            if (this.id != ""){
                console.log(this.id);
                this.getArticle();
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

            imgReader: function (item){
                let blob = item.getAsFile();
                let reader = new FileReader();
                let ret = "";
                reader.onload = function(e){
                };
                reader.readAsDataURL(blob);
                return reader;
            },

            // 获取文章id
            getId: function(){
                let url = document.URL;
                let arr = url.split("/");
                if (arr[arr.length - 1] != "new"){
                    this.id = parseInt(arr[arr.length - 2]);
                }
            },

            // 获取文章内容
            getArticle: function(){
                let api = "/api/articles/" + this.id;
                axios.get(api, {})
                .then((response) => {
                    if (response.status === 200){
                        this.title = response.data.title;
                        this.content = response.data.content;
                    }else{
                        this.$message.error(response.data);
                    }
                }).catch(error => {
                    this.$message.error(error.response.data.message);
                });
            },

            //粘贴截图
            pasteImage: async function(e){
                let clipboardData = e.clipboardData;

                if(clipboardData){
                    let items = clipboardData.items;
                    let types = clipboardData.types || [];
                    if(!items){
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
                        let reader = this.imgReader(item);
                        await this.sleep(50);
                        axios.post("/api/pics", {base64Code: reader.result})
                        .then((response) => {
                            let index = this.getCursortPosition(document.getElementById("mdeditor"));
                            this.content = this.content.slice(0, index) + "![图片](" + response.data + ")\n" + this.content.slice(index);
                        });
                    }
                }
            },

            getCursortPosition: function(ctrl) {//获取光标位置函数
                var CaretPos = 0;
                // IE Support
                if (document.selection) {
                    ctrl.focus ();
                    var Sel = document.selection.createRange ();
                    Sel.moveStart ('character', -ctrl.value.length);
                    CaretPos = Sel.text.length;
                }
                // Firefox support
                else if (ctrl.selectionStart || ctrl.selectionStart == '0')
                    CaretPos = ctrl.selectionStart;
                return (CaretPos);
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

                /*
                let api = "/api/articles/" + this.id;
                axios.put(api, {
                    content: this.content,
                    title: this.title,
                }).then(function (response){
                    window.location.href = response.data;
                })
                .catch(function (error) {
                    console.log(error);
                });
                */
                let api = "";
                let method = "";
                if (this.id != ""){
                    api = "/api/articles/" + this.id;
                    method = "put";
                }else{
                    api = "/api/articles";
                    method = "post";
                }

                axios({
                    method: method,
                    url: api,
                    data: {title: this.title, content: this.content},
                }).then((response) => {
                    if (response.status === 200){
                        window.location.href = response.data;
                    }else{
                        this.$message.error(response.data);
                    }
                }).catch(error => {
                    this.$message.error(error.response.data);
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
                await this.sleep(10);
                e.target.setSelectionRange(point + spaces.length + 1, point + spaces.length + 1);
            },

            sleep: function(ms){
                return new Promise(resolve => setTimeout(resolve, ms));
            },

            tab: async function(e){
                e.preventDefault();
                let $el = e.target;
                let position = $el.selectionStart + 4;
                this.content = $el.value.substr(0, $el.selectionStart) + '    ' + $el.value.substr($el.selectionStart);
                await this.sleep(10);

                $el.selectionStart = position;
                $el.selectionEnd = position;
                $el.focus();
            },
        },
    });
});
