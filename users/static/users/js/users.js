/* =====================================
  Uploaded Icon Preview
======================================*/
$(function(){
  //画像ファイルプレビュー表示のイベント追加 fileを選択時に発火するイベントを登録
  $('form').on('change', 'input[type="file"]', function(e) {
    var file = e.target.files[0],
        reader = new FileReader(),
        $preview = $(".preview");
        t = this;

    // 画像ファイル以外の場合は何もしない
    if(file.type.indexOf("image") < 0){
      return false;
    }

    // ファイル読み込みが完了した際のイベント登録
    reader.onload = (function(file) {
      return function(e) {
        //既存のプレビューを削除
        $preview.empty();
        // .prevewの領域の中にロードした画像を表示するimageタグを追加
        $preview.append($('<img>').attr({
                  src: e.target.result,
                  width: "150px",
                  class: "preview",
                  title: file.name
              }));
      };
    })(file);

    reader.readAsDataURL(file);
  });
});


/* =====================================
  Pop up menu @ detail
======================================*/
$(function(){
  //appends an "active" class to .popup and .popup-content when the "Open" button is clicked
  $("#open-popup").on("click", function(e){
      $(".popup-overlay, .popup-content").addClass("active");
  });

  //removes the "active" class to .popup and .popup-content when the "Close" button is clicked
  $("#close-popup").on("click", function(e){
      $(".popup-overlay, .popup-content").removeClass("active");
  });
});

/* =====================================
 Infinite Scroll
======================================*/
var infinite = new Waypoint.Infinite({
  element: $('.infinite-container')[0],
  onBeforePageLoad: function () {
    $('.loading').show();
  },
  onAfterPageLoad: function ($items) {
    $('.loading').hide();
  }
});
