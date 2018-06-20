$(document).ready(function () {
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    $('.carousel').carousel({
        "noWrap": true,
        "numVisible": 3,
        "shift": -30,
    });
    $(window).click(function () {
        $('.cardbuttons').slideUp();
        $('.deckbuttons').slideUp();
    });
    $(".cardbuttons").click(function () {
        event.stopPropagation();
    })
    $(".cardsvg").click(function (event) {
        event.stopPropagation();
        var cardid = this.id.substr(7);
        $('.deckbuttons').slideUp();
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
        var cardid = this.id.substr(7);
        if (deckname != "") {
            $.ajaxSetup({
                beforeSend: function (xhr, settings) {
                    if (!(/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type)) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });
            $.post("/newdeck", { name: deckname, cardid: cardid }).done(function (data) {
                if (data == "success") {
                    location.reload();
                } else {
                    console.log("failure");
                }
            });
        }
    });
    $(".deletedeck").click(function () {
        var deckid = this.id.substr(10);
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!(/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type)) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
        $.post("/deletedeck", { deckid: deckid }).done(function (data) {
            if (data == "success") {
                $("#decksection" + deckid).remove();
            } else {

            }
        });
    });
    $(".addtodeck").click(function () {
        var cardid = this.id.substr(3);
        var deckid = this.title.substr(4);
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
    $(".addtags").click(function () {
        var tags = prompt("New tags, separated by commas:");
        var deckid = this.id.substr(7);
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!(/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type)) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
        $.post("/addtagstodeck", { deckid: deckid, tags: tags }).done(function (data) {
            if (data == "success") {
                $("#decktags" + deckid).html(tags);
            } else {

            }
        });
    });
    $(".deckbuttons").click(function () {
        event.stopPropagation();
    })
    $(".decksection").click(function () {
        event.stopPropagation();
        var deckid = this.id.substr(11);
        console.log(deckid);
        $('.cardbuttons').slideUp();
        $('.deckbuttons:not(#deck' + deckid + 'buttons)').slideUp();
        $(this).children('#deck' + deckid + 'buttons').slideToggle();
    });
    $(".decktags, .cardtags").click(function() {
        alert($(this).html());
    })
});