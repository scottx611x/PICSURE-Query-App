/**
 * Created by scott on 9/14/17.
 */
$(document).ready(function(){

    $("#submit").click(function(e){
        // Prevent default form submission behavior of a page reload
        e.preventDefault();

        // Gather values set in form
        var aflQuery = $("#afl-input").val();
        console.log(aflQuery);
        window.location.replace('/table?query='+ aflQuery);
    });
});
