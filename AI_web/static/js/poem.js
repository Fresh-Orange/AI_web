$(document).ready(function () {
    poem_init()
});

function poem_init() {
    $("#btn-run-free").unbind('click').bind('click', function () {
        var submit_data = {"prime": ""};
        $("#btn-run-free").waitMe({});
        $.ajax({
            url: "./sample_poem",
            data: submit_data,
            type: "POST",
        }).done(function (data) {
            $("#btn-run-free").waitMe("hide");
            var dataObj = eval("(" + data + ")");// 转换为json
            var parent = document.getElementById("poem_container");
            parent.appendChild(document.createElement("br"));
            var p = document.createElement("p");

            p.innerText = dataObj["poem"];
            parent.appendChild(p);
        }).fail(function (jqXHR, textStatus, errorThrown) {
            alert('运行失败，请重试')
        });
    });

    $("#btn-run-prime").unbind('click').bind('click', function () {
        var prime_text = $("#prime_input").val();
        var submit_data = {"prime": prime_text};
        $("#btn-run-prime").waitMe({});
        $.ajax({
            url: "./sample_poem",
            data: submit_data,
            type: "POST",
        }).done(function (data) {
            $("#btn-run-prime").waitMe("hide");
            var dataObj = eval("(" + data + ")");// 转换为json
            var parent = document.getElementById("poem_container");

            parent.appendChild(document.createElement("br"));

            var p = document.createElement("p");
            p.innerText = dataObj["poem"];
            parent.appendChild(p);
        }).fail(function (jqXHR, textStatus, errorThrown) {
            alert('运行失败，请重试')
        });
    });


}