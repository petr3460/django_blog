
$('#like').click(function(){
    $.ajax({
                type: "POST",
                url: "{% url 'like' %}",
                data: {'id': $(this).attr('name'), 'csrfmiddlewaretoken': '{{ csrf_token }}'},
                dataType: "json",
                success: function(response) {
                        $('#lc').text(response.likes_count);                            
                },
                error: function(rs, e) {
                        alert(rs.responseText);
                }
            }); 
})
