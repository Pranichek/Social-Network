document.addEventListener('DOMContentLoaded', () => {
    const inputs = document.querySelectorAll('.confirm-number');
    const submitBtn = document.getElementById('submit-confirm');
    const form = document.getElementById('email-confirm-form');

    if (inputs.length === 0) {
        console.error("Поля с классом .code-input не найдены!");
        return;
    }

    function initFirstInput() {
        const first = inputs[0];
        first.disabled = false; 
        
        // Попытка 1: через 100мс
        setTimeout(() => {
            first.focus();
            console.log("Попытка фокуса 1 (100ms)");
        }, 100);

        
        setTimeout(() => {
            first.focus();
            console.log("Попытка фокуса 2 (500ms)");
        }, 500);

       
        setTimeout(() => {
            if (document.activeElement !== first) {
                first.focus();
                console.log("Попытка фокуса 3 (1000ms)");
            }
        }, 1000);
    }
    initFirstInput();

    
    inputs.forEach((input, index) => {
        
        input.addEventListener('input', (e) => {
            
            input.value = input.value.replace(/[^0-9]/g, '');

            if (input.value.length === 1 && index < inputs.length - 1) {
               
                inputs[index + 1].disabled = false;
                inputs[index + 1].focus();
            }
        });

        
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Backspace' && input.value === '' && index > 0) {
                
                input.disabled = true;
                inputs[index - 1].focus();
            }
        });

        
        input.addEventListener('click', () => {
            if (input.disabled) {
                const firstEmpty = Array.from(inputs).find(inp => !inp.value);
                if (firstEmpty) firstEmpty.focus();
            }
        });
    });


    if (submitBtn) {
        submitBtn.addEventListener('click', () => {
            const fullCode = Array.from(inputs).map(i => i.value).join('');
            if (fullCode.length === 6) {
                console.log("Отправка кода:", fullCode);
                form.submit();
            } else {
                alert("Будь ласка, введіть усі 6 цифр коду");
            }
        });
    }
});