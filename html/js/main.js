interval = 0;

function change_tab(id, animation = true) {
    $('.tab.select').removeClass('select');
    $('#' + id).addClass('select');
    e = $('li.' + id);
    transformx = e.index() * e.outerWidth(true);
    if (animation) {
        $('.main .contents').animate({
            'top': '-' + transformx + 'px'
        }, {
            step: function (now, fx) {
                $(this).css({
                    "transform": "translate3d(" + now + "px, 0px, 0px)",
                });
            }
        }, 1000)
    } else {
        $('.main .contents').css({
            "transform": "translate3d(-" + transformx + "px, 0px, 0px)",
            'top': '-' + transformx + 'px'
        });
    }
}
function randint(st, ed) {
    return st + parseInt(Math.random() * (ed - st + 1))
}
// number
number_state = 0, st = 0, ed = 0, s1 = null, s2 = null;
function number_start() {
    number_state = 1;
    $('.number .settings input[type=number]').attr('disabled', 'disabled')
    $('.number .control input').val('停止');
    $('.roll span').addClass('select')
    st = parseInt($('input[type=number].start').val());
    ed = parseInt($('input[type=number].end').val());
    ten = [parseInt(st / 10), parseInt(ed / 10)]
    interval = setInterval(function () {
        s1.text(randint(ten[0], ten[1]))
        s2.text(randint(0, 9))
    }, 1000 / 12)
}
function number_stop() {
    number_state = 0;
    $('.number .settings input[type=number]').removeAttr('disabled')
    $('.number .control input').val('开始');
    clearInterval(interval)
    number = randint(st, ed);
    s1.text(parseInt(number / 10));
    s2.text(number % 10);
    $('.roll span').removeClass('select')
}
function number_toggle() {
    if (number_state == 0) {
        number_start();
    } else if (number_state == 1) {
        number_stop();
    }
}
// --
// name
name_state = 0, xlsx = '', s = null;
function name_start() {
    name_state = 1;
    $('.name .settings select').attr('disabled', 'disabled')
    $('.name .control input').val('停止');
    $('.roll span').addClass('select')
    xlsx = $('.name .settings select').val();
    interval = setInterval(function () {
        s.text(
            window.name_lists[xlsx][randint(0, window.name_lists[xlsx].length - 1)]['name']
        )
    }, 1000 / 12)
}
function name_stop() {
    name_state = 0;
    $('.name .settings select').removeAttr('disabled')
    $('.name .control input').val('开始');
    clearInterval(interval);
    s.text(
        window.name_lists[xlsx][randint(0, window.name_lists[xlsx].length - 1)]['name']
    )
    $('.roll span').removeClass('select')
}
function name_toggle() {
    if (name_state == 0) {
        name_start();
    } else if (name_state == 1) {
        name_stop();
    }
}
function load_lists() {
    $('.name .settings select').empty()
    for (i in window.name_lists) {
        option = document.createElement('option');
        option.value = i;
        option.innerText = i;
        $('.name .settings select').append(option);
    }
}
// --
// function check_hash() {
//     type = window.location.hash.replace('#', '')
//     change_tab(type, false)
// }


$(document).ready(function () {
    // check_hash();
    s1 = $('.number .roll span:first-child');
    s2 = $('.number .roll span:last-child');
    s = $('.name .roll span');
    $('.tab').on('click', function (e) {
        change_tab(e.target.id)
        clearInterval(interval);
        $('.roll span').removeClass('select');
    })
    $('.number .control input').on('click', function () {
        number_toggle()
    })
    $('.name .control input').on('click', function () {
        name_toggle()
    })
    $('.name .settings select').on('change', function () {
        s.text('未开始');
    })
    load_lists();
    $('#reload').on('click', function (e) {
        $(this).addClass('select');
        window.location.reload();
        load_lists();
        $(this).removeClass('select');
    });
})