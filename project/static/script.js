$(function(){
    $("#add").click(function(){
    var last_input = $('input[type="text"]:last');
    var type = last_input.attr("type");
    var name = last_input.attr("name");
    var num = parseInt(name.replace("name", ""));
    $("#container").append('<input type="'+type+'" name="name'+(num+1)+'">');
    })
})