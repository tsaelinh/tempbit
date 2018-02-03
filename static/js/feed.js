$(document).ready(function(){

    var api = "https://api.nytimes.com/svc/mostpopular/v2/mostshared/all-sections/7.json";
    api += '?' + $.param({
      'api-key': "1bf386383447418c80e23ea58ea30e9b"
    });

    $.ajax({
        url: api,
        success: function(data, status) {
            for (var i = 0; i < 20; ++i)
            {
                var htmlString = '<div>';
                htmlString += '<a id="nytimes-' + i + '" href="'+ data.results[i].url +'">'+data.results[i].title+ ' </a>';
                htmlString += '<p><small>' + data.results[i].section + '  |  ' + data.results[i].published_date + '</small></p>';
                htmlString += '</div>';
                $("#feed").append(htmlString);
            }
        },
        dataType: "json"
    });
})
