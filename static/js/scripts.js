document.getElementById('movieForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const movieName = document.getElementById('movieInput').value;
    const response = await fetch('/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ movie: movieName })
    });

    const recommendations = await response.json();
    const recommendationList = document.getElementById('recommendationList');
    recommendationList.innerHTML = '';

    if(recommendations.length > 0){
    recommendations.forEach((movie)=>{
        const li =document.createElement('li');
        li.textContent=movie;
        recommendationList.appendChild(li)
    });
    } else{
        recommendationList.innerHTML = '<li>No recommendations found.</li>';
    }})

