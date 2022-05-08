
let number_state = 0, st = 0, ed = 0, s1 = null, s2 = null;
let name_state = 0, xlsx = null, s = null;
let list1 = [], list2 = [];
let interval;


function random(){
  const array = new Uint32Array(1),
        maxUint = 0xffffffff + 1
  const randomNum = crypto.getRandomValues(array)[0] / maxUint
  return randomNum
}
// AES-ECB 解密
function decrypt(data, key) {
    let key1 = CryptoJS.enc.Utf8.parse(key);
    let encryptedHexStr = CryptoJS.enc.Hex.parse(data);
    let encryptedBase64Str = CryptoJS.enc.Base64.stringify(encryptedHexStr);
    let decrypted = CryptoJS.AES.decrypt(encryptedBase64Str, key1, {
        mode: CryptoJS.mode.ECB,
        padding: CryptoJS.pad.ZeroPadding
    });
    return decrypted.toString(CryptoJS.enc.Utf8);
}

interval = 0;

// 修改模式
function change_tab(id, animation = true) {
    $('.tab.select').removeClass('select');
    $('#' + id).addClass('select');
    let e = $('li.' + id);
    let transformx = e.index() * e.outerWidth(true);
    if (animation) {
        $('.main .contents').animate({
            'top': '-' + transformx + 'px'
        }, {
            step: function (now, fx) {
                $(this).css({
                    "transform": "translate3d(" + now + "px, 0px, 0px)",
                });
            }
        }, 1000);
    } else {
        $('.main .contents').css({
            "transform": "translate3d(-" + transformx + "px, 0px, 0px)",
            'top': '-' + transformx + 'px'
        });
    }
}

// 随机数
function randint(st, ed) {
    return st + Math.floor(random() * (ed - st + 1));
}



function number_start() {
    number_state = 1;
    $('.number .settings input[type=number]').attr('disabled', 'disabled');
    $('.number .control input').val('停止');
    $('.roll span').addClass('select')
    st = parseInt($('input[type=number].start').val());
    ed = parseInt($('input[type=number].end').val());
    let ten = [Math.floor(st / 10), Math.floor(ed / 10)]
    interval = setInterval(function () {
        let number = randint(st, ed);
        s1.text(Math.floor(number / 10));
        s2.text(number % 10);
    }, 1000 / 12)
}

function number_stop() {
    number_state = 0;
    $('.number .settings input[type=number]').removeAttr('disabled')
    $('.number .control input').val('开始');
    clearInterval(interval)
    let number = randint(st, ed);
    s1.text(Math.floor(number / 10));
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

// 解密名单
function list_decrypt(key) {
    if (window.name_lists == undefined || window.name_lists.length == 0) return;

    let tip = $('.name .tip');
    tip.text('正在解密名单...');
    try {
        for (let i in window.name_lists) {
            let decr = decrypt(window.name_lists[i], key);
            window.name_lists[i] = JSON.parse(decr).data;
        }
        change_list();
    } catch {
        tip.text('名单解密失败！请重启程序再试！');
    }
    tip.text('名单解密成功！');
    setTimeout(function () {
        tip.animate({
            'opacity': 0
        }, 1500, function () {
            $(this).hide();
        });
    });
}



function name_next(){
    let index = randint(0, list1.length - 1);
    s.text(list1[index]['name']);
    list2.push(list1[index]);
    list1.splice(index, 1);
    if(list1.length == 0){
        list1 = list2;
        list2 = [];
    }
}

function name_start() {
    name_state = 1;
    $('.name .settings select').attr('disabled', 'disabled')
    $('.name .control input').val('停止');
    $('.roll span').addClass('select')
    interval = setInterval(
        name_next
    //     function () {
    //     s.text(
    //         window.name_lists[xlsx][randint(0, window.name_lists[xlsx].length - 1)]['name']
    //     )
    // }
    , 1000 / 12);
}

function name_stop() {
    name_state = 0;
    $('.name .settings select').removeAttr('disabled')
    $('.name .control input').val('开始');
    clearInterval(interval);
    name_next();
    // s.text(
    //     window.name_lists[xlsx][randint(0, window.name_lists[xlsx].length - 1)]['name']
    // );
    $('.roll span').removeClass('select');
}

function name_toggle() {
    if (name_state == 0) {
        name_start();
    } else if (name_state == 1) {
        name_stop();
    }
}

// 加载名单
function load_lists() {
    $('.name .settings select').empty();
    if (window.name_lists == undefined || window.name_lists.length == 0) {
        $('.name .tip').text('未找到名单');
        $('.name .control input').attr('disabled', 'disabled');
        $('.name .settings select').attr('disabled', 'disabled');
    }
    for (let i in window.name_lists) {
        let option = document.createElement('option');
        option.value = i;
        option.innerText = i;
        $('.name .settings select').append(option);
    }
}


function change_list() {
    xlsx = $('.name .settings select').val();
    list1 = JSON.parse(JSON.stringify(window.name_lists[xlsx]));
    list2 = [];
}

$(document).ready(function () {
    s1 = $('.number .roll span:first-child');
    s2 = $('.number .roll span:last-child');
    s = $('.name .roll span');
    $('.tab').on('click', function (e) {
        change_tab(e.target.id)
        clearInterval(interval);
        $('.roll span').removeClass('select');
    });
    $('.number .control input').on('click', number_toggle);
    $('.name .control input').on('click', name_toggle);
    $('.name .settings select').on('change', function () {
        s.text('未开始');
        change_list();
    });
    load_lists();
    $('#reload').on('click', function (e) {
        $(this).addClass('select');
        window.location.reload();
        load_lists();
        $(this).removeClass('select');
    });
});

