$(document).ready(function(){
  $(function() {
    setTimeout(function() { 
       $('.container').addClass('loaded'); 
    }, 2000)  
  })
  // 還本型 循環型切換
  $("input[type='radio'][name='type']").change(function(){
     // var type = $("input[type='radio'][name='type']:checked").val()
    if (this.value == "1"){
      $("#chooseType").text("還本型")
      $("input[type='radio'][name='stage']")[1].checked = true;
	    $(".stageType2").css("display", "inline-block")
	    $(".stageType").css("width", "45%")
      $("#secperiod").css("display", "inline-block")
      $("#firstperiod").css("margin-top", "10px")
      var loanPeriod = parseInt($("#loanPeriod").val())
      secPeriodTwo.value = loanPeriod*12
      var firstInputPeriod = parseInt($("#firstPeriodTwo").val())
      secPeriodOne.value = firstInputPeriod + 1
      document.getElementById('firstPeriodTwo').disabled=false
      document.getElementById('secPeriodTwo').disabled=true
      document.getElementById('secPeriodOne').disabled=true
    }else{
      $("#chooseType").text("循環型")
      $("input[type='radio'][name='stage']")[0].checked = true;
	    $(".stageType2").css("display", "none")
	    $(".stageType").css("width", "100%")
      $("#secperiod").css("display", "none")
      var width = $(window).width()
      if (width < 675){
        $("#firstperiod").css("margin-top", "0px")
      }else{
        $("#firstperiod").css("margin-top", "35px")
      }
      var loanPeriod = parseInt($("#loanPeriod").val())
      firstPeriodTwo.value = loanPeriod*12
      document.getElementById('firstPeriodTwo').disabled=true
    }
  })
  
  // 階段式選擇切換
  $("input[type='radio'][name='stage']").change(function(){
    if (this.value == "a"){
      $("#secperiod").css("display", "none")
      var width = $(window).width()
      if (width < 675){
        $("#firstperiod").css("margin-top", "0px")
      }else{
        $("#firstperiod").css("margin-top", "35px")
      }
      var loanPeriod = parseInt($("#loanPeriod").val())
      firstPeriodTwo.value = loanPeriod*12
    }else{
      $("#secperiod").css("display", "inline-block")
      $("#firstperiod").css("margin-top", "10px")
      var loanPeriod = parseInt($("#loanPeriod").val())
      secPeriodTwo.value = loanPeriod*12
      var firstInputPeriod = parseInt($("#firstPeriodTwo").val())
      secPeriodOne.value = firstInputPeriod + 1
    }
  })
  
  // 更改貸款期間
  $("#loanPeriod").on('input', function(){
    var stage = $("input[type='radio'][name='stage']:checked").val()
    if (stage == "b"){
	  // 兩段式
      var loanPeriod = parseInt($("#loanPeriod").val())
      secPeriodTwo.value = loanPeriod*12
    }else{
	  // 一段式
      var loanPeriod = parseInt($("#loanPeriod").val())
      firstPeriodTwo.value = loanPeriod*12
    }
    
  })
  
  // 二階段輸入月份
  $("#firstPeriodTwo").on('input', function(){
    var stage = $("input[type='radio'][name='stage']:checked").val()
    if (stage == "b"){
      var firstInputPeriod = parseInt(this.value)
      secPeriodOne.value = firstInputPeriod + 1
    }else{
      console.log("stageA，DoingNothing")
    }

  });
});

$("#clear").click(function(){
  event.preventDefault();
  $("#calcuForm")[0].reset();
  $('#thead tbody').empty();
  document.getElementById('secPeriodTwo').disabled=true
  document.getElementById('secPeriodOne').disabled=true
  $("#resultPercent").empty();
})

// 開始試算btn
$("#mainSubmit").click(function(e){
  e.preventDefault();
  console.log("clickSubmit")
  // var stage = $("input[type='radio'][name='stage']:checked").val()
  // console.log(stage)
  // console.log(parseInt($("#loanPeriod").val()))
  // console.log(parseInt($("#firstPeriodTwo").val()))
  // console.log(parseInt($("#secPeriodTwo").val()))
  document.getElementById('secPeriodTwo').disabled=false
  document.getElementById('secPeriodOne').disabled=false
  $.ajax({
    url: '/',
    type: 'post',
    data: $("#calcuForm").serialize(),
    dataType: 'json',
    success:function(response){
      console.log("SUCCESS")
      // $("html, body").css("overflow-y", "auto");
      $("#result").show();
      var width = $(window).width()
      if (width > 1200){
        $("#calcuForm").css("top", "60%");
      }else if (width > 650){
        $("#calcuForm").css("top", "35%");
      }else if (width < 320){
        $("#calcuForm").css("top", "130%");
      }else{
        if(width <= 375){
          $("#calcuForm").css("top", "680px");// 375px
        }else{
          $("#calcuForm").css("top", "100%"); //414px
        }
      }
      // console.log(response)
      console.log(response['ans'])
      console.log(typeof(response['ans']))
      // render利率
      var rateAns = response['ans'].toFixed(4)
      $("#resultPercent").text(rateAns)

      // renderTable
      var tableAns = JSON.parse(response['table'])
      var table_title_template = "<table class='dataframe data' id='thead' border='1'><thead><tr><th>期別</th><th>應還本金</th><th>應付利息</th><th>應付本息</th><th>剩餘本金</th></tr></thead></table>"
      var tbody_template = "<tbody><tr><td>{{num}}</td><td>{{first}}</td><td>{{sec}}</td><td>{{third}}</td><td>{{forth}}</td></tr></tbody>"
      console.log(tableAns)
      console.log(tableAns['columns'][0]) //抓欄位名稱 0~4
      console.log(tableAns['data'][0][4]) // 抓數值 0~4 共五個
      var renderData = tableAns['data']
      $("#bottom").html(table_title_template)
      for (var i=0; i<renderData.length; i++){
          console.log(renderData[i][2])
          var now_template=tbody_template.replace("{{num}}", renderData[i][0])
                                         .replace("{{first}}", renderData[i][1])
                                         .replace("{{sec}}", renderData[i][2])
                                         .replace("{{third}}", renderData[i][3])
                                         .replace("{{forth}}", renderData[i][4]);
          console.log(now_template)
          $("#thead").append(now_template)                                     
      }
      // console.log(now_template)
    }
  })
  // alert($(this).text())
  
  // $("#result").show();
  // $("#calcuForm").css("top", "35%");
  // console.log(secPeriodTwo.value)
})
