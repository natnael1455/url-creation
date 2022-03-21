import $ from 'jquery-slim';

let pay_load = {};
// url creating function
const create_url = () => {
    let url = 'https://t.me/kamata_staging_bot?start=';
    let pay_loads = 'o_x';
    let i = 0;
    for (let key in pay_load) {
        let short_code = key.replace(/\s/g, '');
        let value = pay_load[key];
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
        let URL = url + pay_loads;
        window.open(URL, '_blank');
    }
};

// SHOPPING CART PLUS OR MINUS
$('a.qty-minus').on('click', (event) => {
    event.preventDefault();
    let $this = $(event.currentTarget);
    let parent = $this.closest('div').attr('id');
    let price = parseFloat($this.parent().parent().children('#price').text());
    let pro_total = $this.parent().parent().children('#pro-total');
    let $input = $this.closest('div').find('#qty');
    let value = parseInt($input.val());
    let over_all = $('#over-all');
    let over_all_total = parseFloat(over_all.text());
    if (value > 0) {
        value = value - 1;
        over_all_total = over_all_total - price;
    } else {
        value = 0;
    }
    let total = value * price;
    pro_total.children().text(total.toFixed(2));
    over_all.text(over_all_total.toFixed(2));
    $input.val(value);
    pay_load[parent] = value;
});

$('a.qty-plus').on('click', (event) => {
    event.preventDefault();
    let $this = $(event.currentTarget);
    let parent = $this.parent().attr('id');
    let price = parseFloat($this.parent().parent().children('#price').text());
    let pro_total = $this.parent().parent().children('#pro-total');
    let over_all = $('#over-all');
    let over_all_total = parseFloat(over_all.text());
    let $input = $this.closest('div').find('#qty');
    let value = parseInt($input.val());
    if (value < 100) {
        value = value + 1;
        over_all_total = over_all_total + price;
    } else {
        value = 100;
    }

    let total = value * price;
    pro_total.children().text(total.toFixed(2));
    over_all.text(over_all_total.toFixed(2));
    $input.val(value);
    pay_load[parent] = value;
});

$('a.btn-update').on('click', () => {
    create_url();
});

// RESTRICT INPUTS TO NUMBERS ONLY WITH A MIN OF 0 AND A MAX 100
$('.qty').on('blur', (event) => {
    event.preventDefault();
    let input = $(event.currentTarget);
    let value = parseInt($(event.currentTarget).val());

    if (value < 0 || isNaN(value)) {
        input.val(0);
    } else if (value > 100) {
        input.val(100);
    }
});

$('.qty').on('focusin', function () {
    console.log($(this).val());
    $(this).data('val', $(this).val());
});

$('.qty').on('change keydown', function (event) {
    let $this = $(event.currentTarget);
    console.log(event.key);
    if (event.type == 'change' || event.key == 'Enter') {
        let prev = $this.data('val');
        let current = $this.val();
        console.log('Prev value ' + prev);
        console.log('New value ' + current);
        let parent = $this.parent().attr('id');
        let price = parseFloat(
            $this.parent().parent().children('#price').text()
        );
        let pro_total = $this.parent().parent().children('#pro-total');
        let over_all = $('#over-all');
        let over_all_total = parseFloat(over_all.text());
        if (current > 100) {
            current = 100;
        } else if (current < 0 || isNaN(current)) {
            current = 0;
        }
        over_all_total = over_all_total + (current - prev) * price;
        let total = current * price;
        pro_total.children().text(total.toFixed(2));
        over_all.text(over_all_total.toFixed(2));
        $this.data('val', current);
        pay_load[parent] = current;
    }
});
