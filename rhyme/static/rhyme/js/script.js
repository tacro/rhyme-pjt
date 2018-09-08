// /* =====================================
//   Like Button Ajax
// ======================================*/
//
// $(function(){
//   function updateText(btn, newCount, verb){
//     btn.text(newCount + " " + verb)
//   }
//
//   $('.like-btn').click(function(e){
//     e.preventDefault()
//     var likeUrl = $(this).attr("data-href")
//     var likeCount = parseInt($(this).attr("data-likes"))
//     var addLike = likeCount + 1
//     var removeLike = likeCount - 1
//     $.ajax({
//       url: likeUrl,
//       method: "GET",
//       data: {},
//       success: function(data){
//         // console.log(data)
//         console.log($(this).text())
//         if (data.liked){
//           updateText($('.like-text'), addLike, "Unlike")
//         } else {
//           updateText($('.like-text'), removeLike, "Like")
//         }
//       }, error: function(error){
//         console.log(error)
//         console.log("error")
//       }
//     })
//   })
// })
