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
            let textClasses = 'fw-bold';

            // change the style and number of columns based on the number of choices.
            if (number_choices == 4) {
                // check if the question type is 'fill blank'.
                if (data.question[0].type == 'fill_blank') {
                    $('#answer-choices').attr('class', 'row row-cols-4');
                    textClasses += ' fs-1';
                } else if (data.choices[0].text.split(' ').length == 1 || data.choices[1].text.split(' ').length == 2) {
                    $('#answer-choices').attr('class', 'row row-cols-2');
                    textClasses += ' fs-1';
                } else if (data.choices[1].text.split(' ').length >= 3) {
                    $('#answer-choices').attr('class', 'row row-cols-1');
                    textClasses += ' fs-1';
                }
            } else if (number_choices == 6) {
                $('#answer-choices').attr('class', 'row row-cols-3');
                textClasses += ' fs-1';
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