const pay_load = {};
const bot = window.Telegram.WebApp;
// url creating function
const create_url = (PayLoad) => {
    const url = 'http://t.me/natis_test_bot?start=';

    const items = Object.entries(PayLoad).reduce((acc, value) => {
        return value[1] !== 0 ? [...acc, `${value[0]}_${value[1]}`] : acc;
    }, []);

    const pay_loads = items.join('_');

    if (pay_loads.length > 64) {
        alert(
            'the size of the payload is more than 64 bytes please remove some items'
        );
    } else if (items.length === 0) {
        alert(
            'the size of the payload is more than 64 bytes please remove some items'
        );
    } else {
        const uri = `${url}o_x${pay_loads}`;
        window.open(uri, '_blank');
    }
};

const send_payload = (PayLoad) => {
    const items = Object.entries(PayLoad).reduce((acc, value) => {
        return value[1] !== 0 ? [...acc, `${value[0]}_${value[1]}`] : acc;
    }, []);

    const pay_loads = items.join('_');

    // checking if the payload with more 64 charters

    //checking if the payload is empty
    if (pay_loads === '') {
        bot.sendData('you did not select any item');
    } else {
        bot.sendData(pay_loads);
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
    create_url(pay_load);
});

$('a.btn-update-blue').on('click', () => {
    send_payload(pay_load);
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
