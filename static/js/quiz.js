document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('quizForm');
    if (form) {
        form.addEventListener('submit', function(event) {
            const radioButtons = form.querySelectorAll('input[name="answer"]');
            let answerSelected = false;
            
            radioButtons.forEach(radio => {
                if (radio.checked) {
                    answerSelected = true;
                    // Mark the selected button
                    const button = radio.parentElement;
                    button.classList.add('selected');
                }
            });
            
            const textInput = form.querySelector('input[type="text"][name="answer"]');
            if (textInput && textInput.value.trim() !== '') {
                answerSelected = true;
            }
            
            if (!answerSelected) {
                event.preventDefault();
                alert('Please select or enter an answer before proceeding.');
                return;
            }

            // Allow form submission to proceed to server
            // The server will handle the next/submit action
        });

        // Enhance option buttons for better UX
        const optionButtons = document.querySelectorAll('.option-button');
        optionButtons.forEach(button => {
            button.addEventListener('click', function() {
                const radio = this.querySelector('input[type="radio"]');
                if (radio) {
                    radio.checked = true;
                    optionButtons.forEach(btn => btn.classList.remove('selected'));
                    this.classList.add('selected');
                }
            });
        });
    }
});