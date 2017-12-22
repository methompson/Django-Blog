function deletePost() {
    //result = document.getElementById("result")
    csrf = document.getElementsByName("csrfmiddlewaretoken")
    //result.innerHTML = csrf[0].value
    //TODO: Provide Modal to confirm deleting post
    //TODO: Redirect or refresh page on success
    var post = jQuery.post(url, {"csrfmiddlewaretoken": csrf[0].value});
    post.done(function(data){
        window.location.replace(data)
    })
    .fail(function(data){
        alert("There was an error: " + data);
    });
}

function setVal(slug){
    url = slug
    
}

function clearVal(){
    url = ""
}

var url = ""