// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};

// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        // Complete as you see fit.
        comment_list: [],
        new_comment: "",
        view: 0,

        markerData: [],
        otherUserID: 0,
        profileData: [],
    };

    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };

    // set user id that you are messaging
    // app.getUser = function (otherUserID) {
    //     app.vue.otherUserID = otherUserID
        

    //     // user id you are messaging
    //     // axios.post(getUserURL, { id: app.vue.otherUserID })
    //     // .then(function (result) {
 
    //     // });

    //     // refresh after user id is set
    //     app.load_messages();
    //     setTimeout(function() {
    //         app.load_messages();
    //     }, 200);
    // };

    // user add message and it gets sent to controller to be stored in DB
    app.add_comment = function () {
        // send the new comment to controller to be added to the db
        axios.post(add_messages_url, {text: app.vue.new_comment})
        
        // clear the type bar
        app.vue.new_comment = "";
        
        // refresh
        app.load_messages();
        setTimeout(function() {
            app.load_messages();
        }, 200);
    };

    // refresh messages, controller makes db query again and vue refreshes the page
    app.load_messages = function () {

        // get the user id being messaged from the controller db
        axios.get(getUserURL)
        .then(function (result) {
            app.vue.otherUserID = result.data.id;
            // console.log(result.data.id);

            // get the comment list based on the user id being messaged
            axios.get(load_messages_url)
            .then(function (comments) {
                // console.log(app.vue.otherUserID);
                app.vue.comment_list = comments.data.comment_list;
            });
        });

    };

    // This contains all the methods.
    app.methods = {
        // Complete as you see fit.
        add_comment: app.add_comment,
        // getUser: app.getUser,
        load_messages: app.load_messages,
    };

    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    // And this initializes it.
    app.init = () => {
        // Put here any initialization code.
        // Typically this is a server GET call to load the data.
        app.load_messages()

    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
