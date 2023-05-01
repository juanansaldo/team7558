var button = document.getElementById('btn');
var search = document.getElementById('search');

searchForm.addEventListener("submit", function(event) {
    event.preventDefault();
    var keyword = searchInput.value;
    localStorage.setItem("keyword", keyword);
    window.location.href = "detail.html";
});