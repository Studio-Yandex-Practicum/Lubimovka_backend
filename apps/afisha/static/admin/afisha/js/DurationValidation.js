'use_strict';
{
    function checkDurationValid(duration) {
        const re = /^0?\d:[0-5]\d:[0-5]\d$/;
        return re.test(duration);
    };

    function showError(input) {
        // delete previous errors to avoid duplication
        var errors = document.querySelectorAll('.durationError');
        for (var i = 0; i < errors.length; i++) {
            errors[i].remove()
        };
        var error = document.createElement('div');
        error.className='durationError';
        error.style.color = 'red';
        error.innerHTML = 'Введите продолжительность в формате ЧЧ:ММ:СС';
        input.parentElement.insertBefore(error, input);
    };

    document.addEventListener('submit', function(e) {
        const durationField = document.getElementById('id_duration');
        if (!checkDurationValid(durationField.value)) {
            e.preventDefault();
            showError(durationField);
            durationField.focus();
        };
    });
};
