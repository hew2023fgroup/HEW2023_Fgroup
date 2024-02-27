document.getElementById('searchInput').addEventListener('click', function() {
    var searchHistory = document.querySelector('.search-history');
    if (searchHistory.style.display === 'none') {
      searchHistory.style.display = 'block';
    } else {
      searchHistory.style.display = 'none';
    }
});

// document.getElementById('closebtn').addEventListener('click', function() {
//   var searchHistory = document.querySelector('.search-history');
//   searchHistory.style.display = 'none';
// });


// document.getElementById("searchInput").addEventListener("keydown", function(event) {
//   var searchHistory = document.querySelector('.search-history');
//   searchHistory.style.display = 'none';
// });

