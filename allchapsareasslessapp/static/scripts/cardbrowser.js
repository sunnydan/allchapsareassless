$(document).ready(function () {
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    $('.carousel').carousel({
        "noWrap": true,
        "numVisible": 3,
        "shift": -30,
    });
    $(window).click(function () {
        $('.cardbuttons').slideUp();
    });
    $(".cardbuttons").click(function () {
        event.stopPropagation();
    })
    $(".cardsvg").click(function (event) {
        event.stopPropagation();
        var cardid = this.id.substr(7);
        $('.cardbuttons:not(#card' + cardid + 'buttons)').slideUp();
        $(this).siblings('#card' + cardid + 'buttons').slideToggle();
    })
    $(".like").click(function () {
        var cardid = this.id.substr(4);
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!(/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type)) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
        $.post("/likecard", { cardid: cardid }).done(function (data) {
            if (data == "success") {
                let i = parseInt($(".likingusers" + cardid).html()) + 1;
                $(".likingusers" + cardid).html(i);
            } else {

            }
        });
    });
    $(".unlike").click(function () {
        var cardid = this.id.substr(6);
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!(/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type)) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
        $.post("/unlikecard", { cardid: cardid }).done(function (data) {
            if (data == "success") {
                let i = parseInt($(".likingusers" + cardid).html()) - 1;
                $(".likingusers" + cardid).html(i);
            } else {

            }
        });
    });
    $(".delete").click(function () {
        var cardid = this.id.substr(6);
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!(/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type)) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
        $.post("/deletecard", { cardid: cardid }).done(function (data) {
            if (data == "success") {
                $("#cardsection" + cardid).remove();
            } else {

            }
        });
    });
    $(".newdeck").click(function () {
        var deckname = prompt("Name for new deck:");
        if (deckname != "") {
            $.ajaxSetup({
                beforeSend: function (xhr, settings) {
                    if (!(/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type)) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });
            $.post("/newdeck", { name: deckname }).done(function (data) {
                if (data == "success") {
                    location.reload();
                } else {
                    console.log("failure");
                }
            });
        }
    });
    $(".addtodeck").click(function () {
        var cardid = this.id.substr(3);
        var deckid = this.title.substr(4);
        var deckname = prompt("Name for new deck:");
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!(/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type)) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
        $.post("/addtodeck", { cardid: cardid, deckid: deckid }).done(function (data) {
            if (data == "success") {
            } else {
                console.log("failure");
            }
        });
    });
});