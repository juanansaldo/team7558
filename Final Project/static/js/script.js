function submitForm(event) {
    event.preventDefault(); // Prevent the form from submitting normally

    const searchQuery = document.getElementById('searchInput').value;
    const url = '/detail/' + searchQuery

    window.location.href = url;
}