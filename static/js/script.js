// Автоматическая прокрутка чата к последнему сообщению
document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chatMessages');
    
    // Прокрутка к последнему сообщению
    function scrollToBottom() {
        if (chatMessages) {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }
    
    // Прокрутка при загрузке страницы
    scrollToBottom();
    
    // Анимация появления кнопок
    const categoryButtons = document.querySelectorAll('.category-buttons .btn');
    categoryButtons.forEach((button, index) => {
        button.style.opacity = '0';
        button.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            button.style.transition = 'all 0.3s ease';
            button.style.opacity = '1';
            button.style.transform = 'translateY(0)';
        }, index * 100);
    });
    
    // Добавление анимации при нажатии на кнопки
    const allButtons = document.querySelectorAll('.btn');
    allButtons.forEach(button => {
        button.addEventListener('click', function() {
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = '';
            }, 100);
        });
    });
    
    // Эффект набора текста для нового сообщения
    const messages = document.querySelectorAll('.message');
    if (messages.length > 0) {
        const lastMessage = messages[messages.length - 1];
        if (lastMessage.classList.contains('bot-message')) {
            const messageContent = lastMessage.querySelector('.message-content');
            const originalText = messageContent.innerHTML;
            
            // Эффект печати только для коротких сообщений
            if (originalText.length < 100) {
                messageContent.innerHTML = '';
                let index = 0;
                
                function typeWriter() {
                    if (index < originalText.length) {
                        messageContent.innerHTML += originalText.charAt(index);
                        index++;
                        setTimeout(typeWriter, 30);
                    }
                }
                
                setTimeout(typeWriter, 300);
            }
        }
    }
    
    // Обработка формы администратора
    const adminForm = document.querySelector('form[action*="add_question"]');
    if (adminForm) {
        adminForm.addEventListener('submit', function(e) {
            const question = document.getElementById('question').value.trim();
            const category = document.getElementById('category').value;
            
            if (!question || !category) {
                e.preventDefault();
                alert('Пожалуйста, заполните все поля!');
                return;
            }
            
            if (question.length < 10) {
                e.preventDefault();
                alert('Вопрос должен содержать минимум 10 символов!');
                return;
            }
            
            // Показать индикатор загрузки
            const submitButton = this.querySelector('button[type="submit"]');
            const originalText = submitButton.innerHTML;
            submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Добавление...';
            submitButton.disabled = true;
            
            // Если форма прошла валидацию, отправляем её
            setTimeout(() => {
                submitButton.innerHTML = originalText;
                submitButton.disabled = false;
            }, 1000);
        });
    }
    
    // Эффект при наведении на аватар бота
    const botAvatar = document.querySelector('.bot-avatar');
    if (botAvatar) {
        botAvatar.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.1) rotate(5deg)';
        });
        
        botAvatar.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1) rotate(0deg)';
        });
    }
    
    // Обработка очистки чата с подтверждением
    const clearChatForm = document.querySelector('form[action*="clear_chat"]');
    if (clearChatForm) {
        clearChatForm.addEventListener('submit', function(e) {
            if (!confirm('Вы уверены, что хотите очистить историю чата?')) {
                e.preventDefault();
            }
        });
    }
    
    // Добавление времени реального времени
    function updateTime() {
        const now = new Date();
        const timeString = now.toLocaleTimeString('ru-RU', { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
        
        const timeElements = document.querySelectorAll('.message-time');
        if (timeElements.length > 0) {
            const lastTimeElement = timeElements[timeElements.length - 1];
            // Обновляем время только если сообщение было отправлено недавно
            const messageTime = lastTimeElement.textContent;
            const currentTime = timeString;
            
            if (Math.abs(new Date() - new Date()) < 60000) { // В пределах минуты
                lastTimeElement.textContent = currentTime;
            }
        }
    }
    
    // Обновление времени каждую минуту
    setInterval(updateTime, 60000);
    
    // Добавление фокуса на поле ввода в админ панели
    const questionInput = document.getElementById('question');
    if (questionInput) {
        questionInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
    }
});

// Функция для показа уведомлений
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.top = '20px';
    notification.style.right = '20px';
    notification.style.zIndex = '9999';
    notification.style.minWidth = '300px';
    
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Автоматическое удаление через 5 секунд
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 5000);
}

// Обработка ошибок JavaScript
window.addEventListener('error', function(e) {
    console.error('JavaScript Error:', e.error);
    showNotification('Произошла ошибка на странице. Попробуйте обновить страницу.', 'danger');
});

// Проверка соединения с интернетом
window.addEventListener('online', function() {
    showNotification('Соединение восстановлено!', 'success');
});

window.addEventListener('offline', function() {
    showNotification('Отсутствует интернет соединение!', 'warning');
});
