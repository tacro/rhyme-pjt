/* =====================================
  Like Button Ajax
======================================*/

// getelementbyid.innnertext can change the text
// do it dynamically


function updateText(btn, id, newCount){
  btn.removeAttr("data-likes")
  btn.attr("data-likes", newCount)
  document.getElementById(id).innerText = newCount
}

$('.like-btn').click(function(e){
  e.preventDefault()
  var likeUrl = $(this).attr("data-href")
  console.log("before update data-likes: " + $(this).attr("data-likes"))
  var likeCount = parseInt($(this).attr("data-likes"))
  console.log("now like counts " + likeCount)
  var addLike = likeCount + 1
  var removeLike = likeCount - 1
  $.ajax({
    url: likeUrl,
    method: "GET",
    data: {},
    success: function(data){
      console.log(data)
      // console.log($(this).text())
      // var newLikes;
      if (data.liked){
        // newLikes = likeCount + 1
        updateText($(this), 'like-text', addLike)
        console.log("data-likes: " + $(this).attr("data-likes"))

      } else {
        // newLikes = likeCount - 1
        updateText($(this), 'like-text', removeLike)
        console.log("data-likes: " + $(this).attr("data-likes"))
      }
    }, error: function(error){
      console.log(error)
      console.log("error")
    }
  })
})
