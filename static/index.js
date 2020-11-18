function sendForm(){
    let url = "/calculate/"
    let form = {
        "price_per_good": $("#pricePerGood").val(),
        "number_of_goods": $("#numberOfGoods").val(),
        "state": $("#state").val()
    };
    $.post({
        url: url,
        headers: {
            "Content-Type": "application/json;"
        },
        data: JSON.stringify(form),
        statusCode: {
            200: (function (data) {
                $("#result").text("Итого: " + data.result);
            }),
            400: (function (data) {
                let textError = "Плохой запрос:<br>"
                 textError = textError + "<ul>"
                for (i=0; i < data.responseJSON.error_msg.length; i++){
                    textError = textError + "<li>"+ data.responseJSON.error_msg[i].msg + "</li>";
                }
                textError = textError + "</ul>"
                $("#error").html(textError);
            }),
            500: (function (data) {

                $("#error").text("Ошибка сервера! Статус: " + data.status);
            })
        }
    })
}