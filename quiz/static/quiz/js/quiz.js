// keep track of the current question.
var question_id_index = 0;

// hold the starting time of the question.
var question_start_time = new Date().getTime();

// hold the answer's of the fill in blanks question.
var fill_blank_answers = [];

$(document).ready(function(){
    // get the first question and its answer choices.
    getQuestionChoices(questions_ids[question_id_index], null);

    // get the demonstrative question and its answer choices.
    if (questions_ids[0] === '2') {
        // hide the question-card.
        $("#question-card").hide();

        $('#first-question-modal').modal('show');
    }
    
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
            // if the question type is "fill blank", store the 
            // fill in blanks answer choice in the fill_blank_answers array.
            if (questions_types[question_id_index] == 'fill blank') {
                // get the choice text.
                let choice_text = $(this).text();
                fill_blank_answers.push(choice_text);
            }
            // get the next question and its answer choices.
            getQuestionChoices(questions_ids[question_id_index], selected_choice);
            
            // increment the question id index.
            question_id_index++;
            // restart the question start time.
            question_start_time = new Date().getTime();
        }
    });

    $('.first-question-choice').on('click', function() {
        // get the value of the button.
        let selected_choice = $(this).val();

        // if the value equal to False, show an alert message.
        if (selected_choice == 'False') {
            $('#incorrect-choice-alert').show();
            setTimeout(() => {
                $('#incorrect-choice-alert').hide();
            }, 1500);
            return;
        } else {
            // if the value equal to True, show an alert message for a while and close the modal.
            $('#correct-choice-alert').show();
            // whait for 2 seconds and close the modal.
            setTimeout(function(){
                $('#first-question-modal').modal('hide');
            }, 1500);
            
            // show the question-card.
            $("#question-card").show();

            // restart the question start time when the modal is closed.
            question_start_time = new Date().getTime();
        }
    });
});

function getQuestionChoices(question_id, choice_id) {
    const data = new FormData();
    data.append('quiz_id', quiz_id);
    data.append('question_id', question_id);
    data.append('choice_id', choice_id);
    data.append('answer_time', new Date().getTime() - question_start_time);
    data.append('next_question_id', questions_ids[question_id_index + 1]);

    fetch(
        get_question_choices_url, 
        {
            method: 'POST',
            body: data
        }
    ).then(
        response => response.json()
    ).then(data => {
        console.log('data: ', data);

        // check if we have not reached the end of the quiz.
        if (data.status != 'success') {
            // if we have reached the end of the quiz, go to the results page.
            // results_url = '/quiz/results/' + quiz_id + '/';
            window.location.href = results_url; 

            console.log(data.status);
            return;
        }
        
        // change the question number.
        $('#question-number').text(question_id_index + 1);

        // change the question instruction.
        $('#question-instruction').text(data.question[0].instruction);

        // check if the question has an image.
        $('#question-image-div').hide();
        if(data.question[0].image){
            $('#question-image').attr('src', data.question[0].image);
            // set the height and width of the image to 300px.
            $('#question-image').css('height', '250px');
            $('#question-image').css('width', '250px');
            $('#question-image-div').show();
        }
        // check if the question has a non empty text.
        $('#question-text').hide();
        if(data.question[0].text !== ''){
            $('#question-text').text(data.question[0].text);
            $('#question-text').show();
        }

        // check if the question has a non empty paragraph.
        $('#question-paragraph').hide();
        if(data.question[0].paragraph !== ''){
            $('#question-paragraph').text(data.question[0].paragraph);
            $('#question-paragraph').show();
        }

        // delete any previous choices.
        $('#answer-choices').empty();

        // loop through the choices and append them to the choices div.
        number_choices = data.choices.length;

        // check if choices are image or text.
        if (data.choices[0].image !== null) {
            // change the grid column size based on the number of choices.
            if (number_choices == 2 || number_choices == 4) {
                $('#answer-choices').attr('class', 'row row-cols-2');
            } else if (number_choices == 3 || number_choices == 6) {
                $('#answer-choices').attr('class', 'row row-cols-3');
            }

            // if the question has an image, add the image to the choices div.
            for (let i = 0; i < number_choices; i++) {
                let choice_id = data.choices[i].id;
                let choice_image = data.choices[i].image;

                $('#answer-choices').append(
                    `<button class="btn btn-default col" name="choice" id="${choice_id}" value="${choice_id}">
                        <img src="${choice_image}" class="img-thumbnail" alt="" style="height:220px; width:220px">
                    </button>`
                );
            }
        } else {
            // style will change based on number of choices, type of question and length of the text.
            let textClasses = 'fw-bold fs-1';

            // change the style and number of columns based on the number of choices.
            if (number_choices == 4) {
                // check if the question type is 'fill blank'.
                if (data.question[0].type == 'fill blank') {
                    $('#answer-choices').attr('class', 'row row-cols-4');
                    
                    // if the fill_blank_answers array is not empty, 
                    // replace every '___' with elements from the fill_blank_answers array.
                    let question_text = data.question[0].text;

                    for (let i = 0; i < fill_blank_answers.length; i++) {
                        question_text = question_text.replace('ـــــ', `<span style="color: forestgreen">${fill_blank_answers[i]}</span>`);
                    }

                    // split the text by '.'
                    let question_text_array = question_text.split('.');
                    if (question_text_array.length > 1) {
                        // set the question text to the second element of the array.
                        $('#question-text').html(question_text_array[1]);
                    } else {
                        // set the question text to whole text.
                        $('#question-text').html(question_text);
                    }
                    
                } else if (data.choices[0].text.split(' ').length == 1 || data.choices[1].text.split(' ').length == 2) {
                    $('#answer-choices').attr('class', 'row row-cols-2');
                } else if (data.choices[1].text.split(' ').length >= 3) {
                    $('#answer-choices').attr('class', 'row row-cols-1');
                }
            } else if (number_choices == 6) {
                $('#answer-choices').attr('class', 'row row-cols-3');
            }

            // if the question has text, add the text to the choices div.
            for (let i = 0; i < number_choices; i++) {
                let choice_id = data.choices[i].id;
                let choice_text = data.choices[i].text;

                $('#answer-choices').append(
                    `<button class="btn btn-default btn-outline-secondary col ${textClasses}" name="choice" id="${choice_id}" value="${choice_id}" style="font-family: 'Tajawal', sans-serif;">
                        ${choice_text}
                    </button>`
                );
            }
        }     
    });
}