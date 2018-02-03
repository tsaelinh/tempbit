$(document).ready(function(){
    $("#signup").click(function(e) {
        e.preventDefault();
        $.ajax({
            url: "/signup",
            type: "POST",
            data: data,
            dataType: "json"
        });
    })

    $("#signin").click(function(e) {
        e.preventDefault();

        $.ajax({
            url: "/signin",
            type: "POST",
            data: data,
            dataType: "json"
        });

    })
})
