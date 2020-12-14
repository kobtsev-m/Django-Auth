function configureForm() {
    // Social account avatar
    const fileInputs = document.querySelectorAll(
        '.fileinput[data-provides=fileinput]'
    );
    if (fileInputs) {
        const setHiddenInputValue = elem => {
            const inputHolder = elem.children[2].children[0];
            const hiddenInput = inputHolder.querySelector('#imgOnChange');
            if (hiddenInput) {
                hiddenInput.value = '1';
            }
        };
        fileInputs.forEach(fileInput => {
            $(fileInput).on('change.bs.fileinput', function () {
                setHiddenInputValue(this);
            });
            $(fileInput).on('clear.bs.fileinput', function () {
                setHiddenInputValue(this);
            });
        });
    }

    // Getting lang from dropdown
    const langElem = document.querySelector('.lang .nav-link');
    const getLang = function () {
        const lang = langElem.innerHTML.trim().slice(0, 2);
        return lang.toLowerCase() + '-' + lang;
    };

    // Date picker config
    const datepicker = $('[data-toggle="datepicker"]');
    if (datepicker) {
        datepicker.datepicker({
            offset: 10,
            format: 'dd.mm.yyyy',
            startView: 2,
            startDate: new Date(1910, 0, 1),
            endDate: new Date(),
            language: getLang(),
        });
    }

    // Inputs hovering
    const inputs = document.querySelectorAll(
        '.input-group .form-control:not(.is-invalid)'
    );
    inputs.forEach(input => {
        input.addEventListener('focus', function () {
            const inputText = this.parentNode.childNodes[1].childNodes[1];
            if (inputText) {
                inputText.style.borderColor = '#80bdff';
            }
        });
        input.addEventListener('blur', function () {
            const inputText = this.parentNode.childNodes[1].childNodes[1];
            if (inputText) {
                inputText.style.borderColor = '#ced4da';
            }
        });
    });
}

document.addEventListener('DOMContentLoaded', _ => {
    if (document.querySelector('form')) {
        configureForm();
    }
});
