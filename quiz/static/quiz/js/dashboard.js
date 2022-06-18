$(document).ready(function () {
    $('#example').DataTable();

    // When the user clicks on the button, log the value of the button
    $('.details-button').on('click', function () {
        var user_id = $(this).val();

        data = new FormData();
        data.append('user_id', user_id);

        // Get the user's detailed results
        fetch(user_detailed_results_url, {
            method: 'POST',
            body: data
        }).then((response) => {
            return response.json();
        }).then((data) => {
            console.log('data: ', data);
            /**
             * Update the modal with the user's details
             */
            $('#firstName').text(data.user.first_name);
            $('#lastName').text(data.user.last_name);
            $('#sex').text(data.user.sex);
            $('#birthDate').text(data.user.birth_date);
            $('#academicDegree').text(data.user.academic_degree);
            $('#aphasiaType').text(data.user.aphasia_type);
            $('#injuryDate').text(data.user.injury_date);
            $('#address').text(data.user.address);
            $('#phoneNumber').text(data.user.phone_number);
            // get the table body with id='resultTableBody'
            var tableBody = document.getElementById('resultTableBody');

            // clear the table body
            tableBody.innerHTML = '';

            // get the number of questions
            var answersLength = data.answers.length;
            for (var i = 0; i < answersLength; i++) {
                // create a new row
                var row = tableBody.insertRow(i);
                // create a new cell
                var cell1 = row.insertCell(0);
                var cell2 = row.insertCell(1);
                var cell3 = row.insertCell(2);
                var cell4 = row.insertCell(3);
                var cell5 = row.insertCell(4);
                // add the question to the cell
                cell1.innerHTML = data.answers[i].qn_id;
                // add the user's answer to the cell
                cell2.innerHTML = data.answers[i].qn_label;
                // add the correct answer to the cell
                cell3.innerHTML = data.answers[i].correct_answer;
                // add the incorrect answer to the cell
                cell4.innerHTML = data.answers[i].user_answer;
                // add the time to the cell
                cell5.innerHTML = data.answers[i].answer_time;
            }
        }).catch((error) => {
            console.log('error: ', error);
        });

        // Open the modal
        $('#user-result-detail-modal').modal('show');
    });

    // When the user clicks on the delete results button, show the confirmation modal
    $('.delete-button').on('click', function () {
        $('#delete-user-answers-modal').modal('toggle');

        // set the user_id to the value of the button
        $('#delete-user-answers-btn').val($(this).val());
    });

    // When the user clicks on the delete user answers button, delete the user's answers.
    $('#delete-user-answers-btn').on('click', function () {
        let user_id = $(this).val();

        data = new FormData();
        data.append('user_id', user_id);

        // Delete the user's answers
        fetch('{% url "delete_user_answers" %}', {
            method: 'POST',
            body: data
        }).then((response) => {
            return response.json();
        }).then((data) => {
            console.log('data: ', data);

            // check if the user's answers were deleted successfully
            if (data.status == 'success') {
                // hide the modal
                $('#delete-user-answers-modal').modal('hide');
                // reload the page
                location.reload();
            } else {
                // show an error message
                alert('حدث خطأ أثناء حذف الإجابات');
            }
            // Reload the page
            location.reload();
        }).catch((error) => {
            console.log('error: ', error);
        });
    });
});