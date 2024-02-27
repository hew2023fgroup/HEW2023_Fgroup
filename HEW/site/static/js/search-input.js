document.getElementById('searchInput').addEventListener('click', function() {
    var searchHistory = document.querySelector('.search-history');
    if (searchHistory.style.display === 'none') {
      searchHistory.style.display = 'block';
    } else {
      searchHistory.style.display = 'none';
    }
});


// document.getElementById('searchInput').addEventListener('click', function() {
//     var searchHistory = document.querySelector('.search-history');
//     if (searchHistory.style.display === 'none') {
//       searchHistory.style.display = 'block';
//       setTimeout(function() {
//         searchHistory.style.opacity = '1';
//       }, 0);
//     } else {
//       searchHistory.style.opacity = '0';
//       setTimeout(function() {
//         searchHistory.style.display = 'none';
//       }, 300);
//     }
// });