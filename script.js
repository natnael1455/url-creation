var pay_load = {};
// url creating function
function create_url() {
    var url = 'https://t.me/kamata_test_bot?start=';
    var pay_loads = 'o_x';
    var i = 0;
    for (let key in pay_load) {
        var short_code = key.replace(/\s/g, '');
        var value = pay_load[key];
        if (value != 0) {
            if (i == 0) {
                pay_loads = pay_loads + '' + short_code + '_' + value;
            } else {
                pay_loads = pay_loads + '_' + short_code + '_' + value;
            }
            i++;
        }
    }
    // checking if the payload with more 64 charters
    if (pay_loads.length > 64) {
        alert(
            'the size of the payload is more than 64 bytes please remove some items'
        );
    }
    //checking if the payload is empty
    else if (pay_loads === 'o_x') {
        alert('you did not select any item');
    } else {
        var URL = url + pay_loads;
        window.open(URL, '_blank');
    }
}

$('.visibility-cart').on('click', function () {
    var $btn = $(this);
    var $cart = $('.cart');
    console.log($btn);

    if ($btn.hasClass('is-open')) {
        $btn.removeClass('is-open');
        $btn.text('O');
        $cart.removeClass('is-open');
        $cart.addClass('is-closed');
        $btn.addClass('is-closed');
    } else {
        $btn.addClass('is-open');
        $btn.text('X');
        $cart.addClass('is-open');
        $cart.removeClass('is-closed');
        $btn.removeClass('is-closed');
    }
});

// SHOPPING CART PLUS OR MINUS
$('a.qty-minus').on('click', function (e) {
    e.preventDefault();
    var $this = $(this);
    var parent = $this.closest('div').attr('id');
    var price = parseFloat($this.parent().parent().children('#price').text());
    var pro_total = $this.parent().parent().children('#pro-total');
    var $input = $this.closest('div').find('input');
    var value = parseInt($input.val());
    var over_all = $('#over-all');
    var over_all_total = parseFloat(over_all.text());
    if (value > 0) {
        value = value - 1;
        over_all_total = over_all_total - price;
    } else {
        value = 0;
    }
    var total = value * price;
    pro_total.children().text(total.toFixed(2));
    over_all.text(over_all_total.toFixed(2));
    $input.val(value);
    pay_load[parent] = value;
});

$('a.qty-plus').on('click', function (e) {
    e.preventDefault();
    var $this = $(this);
    var parent = $this.parent().attr('id');
    var price = parseFloat($this.parent().parent().children('#price').text());
    var pro_total = $this.parent().parent().children('#pro-total');
    console.log(pro_total);
    var over_all = $('#over-all');
    var over_all_total = parseFloat(over_all.text());
    var $input = $this.closest('div').find('input');
    var value = parseInt($input.val());
    if (value < 100) {
        value = value + 1;
        over_all_total = over_all_total + price;
    } else {
        value = 100;
    }

    var total = value * price;
    console.log(total);
    pro_total.children().text(total.toFixed(2));
    over_all.text(over_all_total.toFixed(2));
    $input.val(value);
    pay_load[parent] = value;
});

$('a.btn-update').on('click', function () {
    create_url();
});
// RESTRICT INPUTS TO NUMBERS ONLY WITH A MIN OF 0 AND A MAX 100
$('input').on('blur', function () {
    var input = $(this);
    var value = parseInt($(this).val());

    if (value < 0 || isNaN(value)) {
        input.val(0);
    } else if (value > 100) {
        input.val(100);
    }
});
