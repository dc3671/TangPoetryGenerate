Vue.prototype.$http = axios;
var app = new Vue({
    el: '#app',
    delimiters: ['${', '}'],
    data: {
        loading: false,
        query: '',
        poem: [' ', ' ', ' ', ' '],
        status: -1,
    },
    methods: {
        get_poem: function() {
            this.poem = [];
            this.loading = true;
            this.$set(this.poem, 0, this.query);
            this.$http.post('/get_poem', {'index':1, 'sentense':this.poem[0]}).then(response => {
                this.$set(this.poem, 1, response.data);
                this.$http.post('/get_poem', {'index':2}).then(response => {
                    this.$set(this.poem, 2, response.data);
                    this.$http.post('/get_poem', {'index':3}).then(response => {
                        this.$set(this.poem, 3, response.data);
                        this.loading = false;
                    });
                });
            });
        },
    }
});
