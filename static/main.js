function showMessageData(messageId){
    // Получение и вывод подробных данных о сообщении
    $("#messageId").html(messageId);
    $.getJSON("/message", {message_id: messageId})
        .done(function(message) {
            $("#typeMessage").html(message.type);
            $("#statusMessage").html(message.status);
            $("#headMessage").html(message.header);
            $("#headRecipients").html(message.recipient);
            $("#tagsMessage").html(message.tags.join());
            $("#textMessage").html(message.body);
            $("#messageModal").modal("show")
        });
}

function updateURLParameter(url, param, paramVal){
    // Обновление GET параметров
    var newAdditionalURL = "";
    var tempArray = url.split("?");
    var baseURL = tempArray[0];
    var additionalURL = tempArray[1];
    var temp = "";
    if (additionalURL) {
        tempArray = additionalURL.split("&");
        for (var i=0; i<tempArray.length; i++){
            if(tempArray[i].split('=')[0] != param){
                newAdditionalURL += temp + tempArray[i];
                temp = "&";
            }
        }
    }
    var rowsText = temp + "" + param + "=" + paramVal;
    return baseURL + "?" + newAdditionalURL + rowsText;
}

$( document ).ready(function() {
    var rowCount = $("#perPage");
    rowCount.val(perPage);
    rowCount.on("change", function() {
        var newUrl = updateURLParameter(window.location.href, 'per_page', this.value);
        window.location.href = updateURLParameter(newUrl, 'page', 1);
    });
});
