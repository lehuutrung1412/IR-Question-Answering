const question_input = document.getElementsByClassName("question-input")[0];
const answer = document.getElementsByClassName("ans")[0];
const textans = document.getElementsByClassName("textans")[0];
const answer_ = document.getElementsByClassName("answer")[0];

question_input.addEventListener("keyup", function(event) {
    if (event.key === "Enter") {
        console.log(question_input.value);
        answer_.style.visibility = "hidden";
        textans.style.visibility = "hidden";
        if (question_input.value === ''){
            alert('Vui lòng nhập câu hỏi!');
        }
        else{
            upload();
        }
    }
});

function upload(){
    let fileForm = new FormData();
    if (question_input.value){
        fileForm.append('question', question_input.value);
    }
    $.ajax({
        method: 'POST',
        url: '/send',
        data: fileForm,
        processData: false,
        cache: false,
        contentType: false,
        success: function (response){
            if (response){
                console.log(response);
                let ans = response['answer'];
                let text = response['text'];
                let start = response['start'];
                let end = response['end'];
                text = text.slice(0, start) + "<strong>" + text.slice(start, end) + "</strong>" + text.slice(end, text.lenght);
                answer.value = ans;
                textans.innerHTML = text;
                answer_.style.visibility = "visible";
                textans.style.visibility = "visible";
            }
            else{
                console.log('No response');
            }
        },
        error: function(error){
            console.log(error);
        }
    });
}