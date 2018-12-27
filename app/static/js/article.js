showdown.setOption('simpleLineBreaks', true);

let app = new Vue({
    el: "#container",
    delimiters: ['[[', ']]'],
    data: {
        id: "",
        title: "",
        content: "",
        converter: new showdown.Converter(),
        editUrl: "",
    },

    created: function(){
        this.get_id();

        this.get_article();
    },

    mounted: function(){},

    updated: function(){
        $('pre code').each(function(i, block){
            hljs.highlightBlock(block);
        });
    },

    methods: {
        get_article: function(){
            let api = "/api/articles/" + this.id;
            axios.get(api, {})
            .then((response) => {
                if (response.status === 200){
                    this.title = response.data.title;
                    this.content = this.converter.makeHtml(response.data.content);
                    this.editUrl = response.data.link + "/edit";
                }else{
                    this.$message.error(response.data);
                }
            }).catch(error => {
                this.$message.error(error.response.data.message);
            });
        },

        get_id: function(){
            let url = document.URL;
            let arr = url.split("/");
            this.id = parseInt(arr[arr.length - 1]);
        },
    },

    watch: {},
});
