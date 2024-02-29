function switchTo(view) {
    if (view === 'grid') {
      document.getElementById('gridView').style.display = 'block';
      document.getElementById('listView').style.display = 'none';
    } else if (view === 'list') {
      document.getElementById('gridView').style.display = 'none';
      document.getElementById('listView').style.display = 'block';
    }
  }