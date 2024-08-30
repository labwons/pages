const url = "http://www.wiseindex.com/DataCenter/GridData?currentPage=1&endDT=2024-08-29&fromDT=2000-01-01&index_ids=WI100&isEnd=1&itemType=1&perPage=10000&term=1";


$(document).ready(async function(){
    try {
      const response = await fetch(url, {
        mode: 'no-cors'
      });
      if (!response.ok) {
          throw new Error('Network response was not ok');
      }
      var src = await response.json();
    } catch (error) {
        console.error('Fetch error:', error);
    }
    console.log(src);
  })