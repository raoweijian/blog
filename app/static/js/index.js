let app = new Vue({
    el: "#container",
    delimiters: ['[[', ']]'],
    data: {
        articles: [],
    },

    created: function(){
        this.get_articles();
    },

    mounted: function(){},

    methods: {
        get_articles: function(){
            axios.get("/api/articles", {})
            .then((response) => {
                if (response.status === 200){
                    this.articles = response.data;
                }else{
                    this.$message.error(response.data);
                }
            }).catch(error => {
                this.$message.error(error.response.data.message);
            });
        },

        deleteArticle: function(id){
            let api = "/api/articles/" + id;
            console.log(api);
            axios.delete(api, {})
            .then((response) => {
                if (response.status === 200){
                    this.get_articles();
                }else{
                    this.$message.error(response.data);
                }
            }).catch(error => {
                this.$message.error(error.response.data.message);
            });
       },
    },

    watch: {},
});
