function expandCard(id, url) {
    let card = document.getElementById(id);
    let originalContent = card.innerHTML;
    let height = card.clientHeight;
    card.innerHTML = `
        <div style="height:${height}px">
            <div id="loader" class="loading-spinner">
                <div class="spinner"></div>
            </div>
        </div>
    `;

    fetch(url)
            .then(response => response.text())
            .then(data => {
                let tempDiv = document.createElement('div');
                tempDiv.innerHTML = data;

                const newContent = tempDiv.querySelector(`.card-body`).outerHTML;

                card.innerHTML = newContent;
            })
            .catch(error => {
                console.error('Error:', error);
                // Revert to original content if there's an error
                card.innerHTML = originalContent;
            });
}