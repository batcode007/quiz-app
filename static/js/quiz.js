document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('quizForm');
    if (form) {
        form.addEventListener('submit', function(event) {
            const radioButtons = form.querySelectorAll('input[name="answer"]');
            let answerSelected = false;
            
            radioButtons.forEach(radio => {
                if (radio.checked) {
                    answerSelected = true;
                }
            });
            
            const textInput = form.querySelector('input[type="text"][name="answer"]');
            if (textInput && textInput.value.trim() !== '') {
                answerSelected = true;
            }
            
            if (!answerSelected) {
                event.preventDefault();
                alert('Please select or enter an answer before proceeding.');
            }
        });
    }
});