// keep track of the current question.
var question_id_index = 0;

// hold the starting time of the question.
var question_start_time = new Date().getTime();

$(document).ready(function(){
    // log all questions ids.
    console.log("questions_ids: ", questions_ids);
    
    // get the first question and its answer choices.
    getQuestionChoices(questions_ids[question_id_index], null);

    // on click of the choice button, get the next question and its answer choices.
    $('#answer-choices').on('click', 'button', function(){
        // get the selected choice.
        let selected_choice = $(this).val();
        console.log('choice btn clicked: ', selected_choice);

        // make sure an answer is selected, if not, show an error message.
        if (selected_choice == null) {
            console.log("Please select an answer.");
            return;
        } else {
            // get the next question and its answer choices.
            getQuestionChoices(questions_ids[question_id_index], selected_choice);
            
            // increment the question id index.
            question_id_index++;
        }
    });
});

