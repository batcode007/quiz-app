// Cricket Quiz App JavaScript

class QuizApp {
    constructor() {
        this.currentQuestion = 0;
        this.score = 0;
        this.timeLeft = 60;
        this.timer = null;
        this.totalTime = 0;
        this.startTime = Date.now();
    }

    async loadQuestion(questionNum) {
        try {
            const response = await fetch(`/get_question/${questionNum}`);
            const question = await response.json();
            
            if (!response.ok) {
                throw new Error(question.error);
            }
            
            this.displayQuestion(question);
            this.startTimer();
        } catch (error) {
            console.error('Error loading question:', error);
            alert('Error loading question');
        }
    }

    displayQuestion(question) {
        const container = document.getElementById('question-container');
        
        let html = `
            <div class="question-card bg-white rounded-lg shadow-lg p-6 mb-6">
                <div class="flex justify-between items-center mb-4">
                    <span class="text-sm font-medium text-gray-500">
                        Question ${question.number} of ${question.total}
                    </span>
                    <div class="text-right">
                        <div class="text-sm text-gray-500">Time Remaining</div>
                        <div id="timer" class="text-2xl font-bold text-green-600">60s</div>
                    </div>
                </div>
                
                <div class="mb-6">
                    <div class="w-full bg-gray-200 rounded-full h-2 mb-4">
                        <div id="timer-progress" class="timer-progress bg-green-500 h-2 rounded-full" style="width: 100%"></div>
                    </div>
                </div>

                <h3 class="text-xl font-semibold text-gray-800 mb-6">${question.text}</h3>
                
                <div id="answer-options" class="space-y-3">
        `;

        if (question.type === 'mcq') {
            question.options.forEach((option, index) => {
                html += `
                    <button class="option-button w-full text-left p-4 rounded-lg border-2 border-gray-200 hover:border-green-500 transition-all"
                            onclick="selectOption('${option}', this)">
                        <span class="font-medium">${String.fromCharCode(65 + index)}.</span> ${option}
                    </button>
                `;
            });
        } else if (question.type === 'true_false') {
            html += `
                <button class="option-button w-full text-left p-4 rounded-lg border-2 border-gray-200 hover:border-green-500 transition-all"
                        onclick="selectOption('True', this)">
                    <span class="font-medium">A.</span> True
                </button>
                <button class="option-button w-full text-left p-4 rounded-lg border-2 border-gray-200 hover:border-green-500 transition-all"
                        onclick="selectOption('False', this)">
                    <span class="font-medium">B.</span> False
                </button>
            `;
        } else if (question.type === 'fill_blank') {
            html += `
                <div class="space-y-4">
                    <input type="text" id="fill-answer" 
                           class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-green-500 focus:outline-none"
                           placeholder="Type your answer here...">
                    <button onclick="submitFillAnswer()" 
                            class="bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 transition-colors">
                        Submit Answer
                    </button>
                </div>
            `;
        }

        html += `
                </div>
            </div>
        `;

        container.innerHTML = html;
        
        // Store question data for submission
        this.currentQuestionData = question;
    }

    startTimer() {
        this.timeLeft = 60;
        this.questionStartTime = Date.now();
        
        this.timer = setInterval(() => {
            this.timeLeft--;
            
            const timerEl = document.getElementById('timer');
            const progressEl = document.getElementById('timer-progress');
            
            timerEl.textContent = `${this.timeLeft}s`;
            progressEl.style.width = `${(this.timeLeft / 60) * 100}%`;
            
            // Warning when less than 10 seconds
            if (this.timeLeft <= 10) {
                timerEl.classList.add('text-red-600');
                progressEl.classList.remove('bg-green-500');
                progressEl.classList.add('bg-red-500');
                
                if (this.timeLeft <= 5) {
                    progressEl.classList.add('timer-warning');
                }
            }
            
            if (this.timeLeft <= 0) {
                this.timeUp();
            }
        }, 1000);
    }

    stopTimer() {
        if (this.timer) {
            clearInterval(this.timer);
            this.timer = null;
        }
    }

    timeUp() {
        this.stopTimer();
        this.submitAnswer('', 60);
    }

    async submitAnswer(answer, timeTaken = null) {
        if (!timeTaken) {
            timeTaken = 60 - this.timeLeft;
        }
        
        this.stopTimer();
        
        try {
            const response = await fetch('/submit_answer', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    question_id: this.currentQuestionData.id,
                    answer: answer,
                    time_taken: timeTaken
                })
            });
            
            const result = await response.json();
            
            if (response.ok) {
                this.showAnswerFeedback(result);
                
                if (result.correct) {
                    this.score++;
                }
                
                // Move to next question after 3 seconds
                setTimeout(() => {
                    this.nextQuestion();
                }, 3000);
            } else {
                alert('Error submitting answer');
            }
        } catch (error) {
            console.error('Error submitting answer:', error);
            alert('Error submitting answer');
        }
    }

    showAnswerFeedback(result) {
        const container = document.getElementById('answer-options');
        const isCorrect = result.correct;
        
        // Disable all option buttons
        const buttons = container.querySelectorAll('.option-button');
        buttons.forEach(btn => {
            btn.disabled = true;
            btn.classList.remove('hover:border-green-500');
        });
        
        // Show feedback
        let feedbackHtml = `
            <div class="mt-6 p-4 rounded-lg ${isCorrect ? 'bg-green-100 border-l-4 border-green-500' : 'bg-red-100 border-l-4 border-red-500'}">
                <div class="flex items-center mb-2">
                    <span class="text-2xl mr-2">${isCorrect ? '✅' : '❌'}</span>
                    <h4 class="font-semibold ${isCorrect ? 'text-green-800' : 'text-red-800'}">
                        ${isCorrect ? 'Correct!' : 'Incorrect'}
                    </h4>
                </div>
                ${!isCorrect ? `<p class="text-gray-700 mb-2"><strong>Correct answer:</strong> ${result.correct_answer}</p>` : ''}
                ${result.explanation ? `<p class="text-gray-600"><strong>Explanation:</strong> ${result.explanation}</p>` : ''}
            </div>
        `;
        
        container.insertAdjacentHTML('beforeend', feedbackHtml);
    }

    async nextQuestion() {
        this.currentQuestion++;
        this.totalTime = Math.floor((Date.now() - this.startTime) / 1000);
        
        if (this.currentQuestion >= 10) {
            await this.finishQuiz();
        } else {
            await this.loadQuestion(this.currentQuestion);
        }
    }

    async finishQuiz() {
        try {
            const response = await fetch('/finish_quiz', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    total_time: this.totalTime
                })
            });
            
            const result = await response.json();
            
            if (response.ok) {
                window.location.href = result.redirect;
            } else {
                alert('Error finishing quiz');
            }
        } catch (error) {
            console.error('Error finishing quiz:', error);
            alert('Error finishing quiz');
        }
    }
}

// Global functions for HTML onclick events
let quizApp;

function selectOption(answer, buttonEl) {
    // Remove previous selection
    document.querySelectorAll('.option-button').forEach(btn => {
        btn.classList.remove('selected');
    });
    
    // Add selection to clicked button
    buttonEl.classList.add('selected');
    
    // Submit answer after short delay
    setTimeout(() => {
        quizApp.submitAnswer(answer);
    }, 500);
}

function submitFillAnswer() {
    const input = document.getElementById('fill-answer');
    const answer = input.value.trim();
    
    if (!answer) {
        alert('Please enter an answer');
        return;
    }
    
    quizApp.submitAnswer(answer);
}

// Initialize quiz when page loads
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('question-container')) {
        quizApp = new QuizApp();
        quizApp.loadQuestion(0);
    }
});
