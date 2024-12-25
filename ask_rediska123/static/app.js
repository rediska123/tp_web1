function getCookie(name) {
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');

        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();

            if (cookie.startsWith(name + '=')) {
                return decodeURIComponent(cookie.substring(name.length + 1));
            }
        }
    }
    return null;
}

const csrftoken = getCookie('csrftoken');

const questions = document.getElementsByClassName('question-card');
for (const card of questions) {
    const likeButton = card.querySelector('.plus-button');
    const dislikeButton = card.querySelector('.minus-button');
    const rating = card.querySelector('.rating-text');
    const id = card.dataset.id;
    //console.log(likeButton) // Для отладки
    //console.log(dislikeButton) // Для отладки
    //console.log(rating) // Для отладки

    likeButton.addEventListener('click', async (event) => {
        const response = await fetch(`/question_like/${id}`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json'
            },
            body: '{ "like_dislike": 1 }'
        });

        if (response.ok) {
            //console.log("QUESTION LIKE") // Для отладки
            const data = await response.json();
            rating.value = data.rating;
        }
    });

    dislikeButton.addEventListener('click', async (event) => {
        const response = await fetch(`/question_like/${id}`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json'
            },
            body: '{ "like_dislike": -1 }'
        });

        if (response.ok) {
            //console.log("QUESTION DISLIKE") // Для отладки
            const data = await response.json();
            rating.value = data.rating;
        }
    });
}

const answers = document.getElementsByClassName('answer-card');
for (const card of answers) {
    const likeButton = card.querySelector('.plus-button');
    const dislikeButton = card.querySelector('.minus-button');
    const rating = card.querySelector('.rating-text');
    const id = card.dataset.id;
    const checkbox = card.querySelector('.answer-checkbox');
    //console.log(likeButton) // Для отладки
    //console.log(dislikeButton) // Для отладки
    //console.log(rating) // Для отладки
    //console.log(checkbox) // Для отладки

    likeButton.addEventListener('click', async (event) => {
        const response = await fetch(`/answer_like/${id}`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json'
            },
            body: '{ "like_dislike": 1 }'
        });

        if (response.ok) {
            //console.log("ANSWER LIKE") // Для отладки
            const data = await response.json();
            rating.value = data.rating;
        }
    });

    dislikeButton.addEventListener('click', async (event) => {
        const response = await fetch(`/answer_like/${id}`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json'
            },
            body: '{ "like_dislike": -1 }'
        });

        if (response.ok) {
            //console.log("ANSWER DISLIKE") // Для отладки
            const data = await response.json();
            rating.value = data.rating;
        }
    });

    checkbox.addEventListener('click', async (event) => {
        const response = await fetch(`/correct_answer/${id}`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json'
            }
        });
    
        if (response.ok) {
            return;
        }
    });

}