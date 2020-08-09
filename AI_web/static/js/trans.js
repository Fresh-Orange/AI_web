

$(document).ready(function(){
  face_init()
});

function face_init() {
    $("#btn-run-man2woman").unbind('click').bind('click', function(){
            var image_path = $("#image-path").text();
            var submit_data = {"model_name": "man2woman", "image_path":image_path};
            $("#changed-image").waitMe({effect : 'win8'});
            $.ajax({
            url: "./change",
            data: submit_data,
            type: "POST",
            }).done(function(data){
                $("#changed-image").waitMe("hide");
                var dataObj=eval("("+data+")");// 转换为json
                var parent = document.getElementById("changed-image");
                parent.innerText = "";
　　　　        // 添加 div
　　　　        var div = document.createElement("img");

　　　　        // 设置 div 属性，如 id
　　　　        div.setAttribute("width", 400);
               div.setAttribute("height", 400);
               div.setAttribute("src", dataObj["src"]);
　　　　        parent.appendChild(div);
            }).fail(function(jqXHR, textStatus, errorThrown){
                alert('运行失败，请重试')
            });
  });

  $("#btn-run-woman2man").unbind('click').bind('click', function(){
            var image_path = $("#image-path").text();
            var submit_data = {"model_name": "woman2man", "image_path":image_path};
            $("#changed-image").waitMe({effect : 'win8'});
            $.ajax({
            url: "./change",
            data: submit_data,
            type: "POST",
            }).done(function(data){
                $("#changed-image").waitMe("hide");
                var dataObj=eval("("+data+")");// 转换为json
                var parent = document.getElementById("changed-image");
                parent.innerText = ""
　　　　        // 添加 div
　　　　        var div = document.createElement("img");

　　　　        // 设置 div 属性，如 id
　　　　        div.setAttribute("width", 400);
               div.setAttribute("height", 400);
               div.setAttribute("src", dataObj["src"]);
　　　　        parent.appendChild(div);
            }).fail(function(jqXHR, textStatus, errorThrown){
                alert('运行失败，请重试')
            });
  });


}