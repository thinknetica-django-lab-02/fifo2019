document.addEventListener('DOMContentLoaded', function() {
    const bodyPage = document.querySelector('body');

    const chatSocket = new WebSocket(`ws://${window.location.host}/ws/chatbot/`);

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);

        console.log(data)

        let text = ''

        if (data.in_stock === '') {
            text = 'Ничего не найдено';
        } else if (data.in_stock === 0) {
            text = 'Товар закончился'
        } else if (data.in_stock > 0) {
            text = `Товар ${data.product_name} в наличии: ${data.in_stock} шт.`
        } else {

        }

        document.querySelector('#chat-log').value += ('> ' + text + '\n');
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

    document.querySelector('#chat-message-input').focus();

    document.querySelector('#chat-message-input').onkeyup = function(e) {
        if (e.keyCode === 13) {  // enter, return
            document.querySelector('#chat-message-submit').click();
        }
    };

    document.querySelector('#chat-message-submit').onclick = function(e) {
        const messageInputDom = document.querySelector('#chat-message-input');
        let message = messageInputDom.value;

        if (!message.match('Наличие #')) {
            let errorText = '> Нет такой команды'
            document.querySelector('#chat-log').value += (errorText + '\n');
            messageInputDom.value = '';
            return false;
        }

        let searchProduct = message.split('#')[1];

        message = searchProduct.trim();

        if (message === '') {
            let errorText = '> Вы не ввели название товара!'
            document.querySelector('#chat-log').value += (errorText + '\n');
            messageInputDom.value = '';
            return false;
        }

        chatSocket.send(JSON.stringify({
            'message': message
        }));

        messageInputDom.value = '';
    };


    function openChat(dataTarget) {

        let textWelcome = '> Это чат бот. Чтобы узнать товара на складе нужно отправить команду: "Наличие #Название_товара"'
        document.querySelector('#chat-log').value += (textWelcome + '\n');

        let chatBlock = document.querySelector('.js-chat-block');

        chatBlock.style.display = 'flex';
        dataTarget.style.display = 'none';
    }


    function closeChat(dataTarget) {

        let chatBlock = document.querySelector('.js-chat-block');
        let chatOpen = document.querySelector('.js-chat-open');

        chatOpen.style.display = 'flex';
        chatBlock.style.display = 'none';
    }


    /**
     * Событие клика
     */
    bodyPage.addEventListener('click', function(event) {
        const dataTarget = event.target;
        dataTarget.classList.contains('js-chat-open') ? openChat(dataTarget) : false;
        dataTarget.classList.contains('js-close-chat') ? closeChat(dataTarget) : false;
    })
})
