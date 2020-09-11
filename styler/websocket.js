// need to change to websocket server's address
var wsUri = "ws://192.168.43.6:9999";
var output;
var work,username;
var server_status;
var stylingType_done;

function init()
{
  output = document.getElementById("output");
  console.log("init");
  print(init);
  testWebSocket();
}
function testWebSocket()
{
  websocket = new WebSocket(wsUri);
  console.log("new socket")
  websocket.onopen = function(evt) { onOpen(evt) };
  websocket.onclose = function(evt) { onClose(evt) };
  websocket.onmessage = function(evt) { onMessage(evt) };
  websocket.onerror = function(evt) { onError(evt) };
}
function onOpen(evt)
{
  console.log("Connected");
  doSend_ticket();
}
function onClose(evt)
{
  console.log("DISCONNECTED");
}
function onMessage(evt)
{
  var message_recv = JSON.parse(evt.data);
  console.log('RESPONSE: ' + message_recv);
  // Call Notification method humere  
  console.log("work name: "+ message_recv.work); //작업의 종류
  console.log("user/work recognized: "+message_recv.username); //인식된 사람 이름.

  work_type = message_recv.work;
  person = message_recv.username;

  if (work_type==0)//receiving information
  {
    console.log(person);
    console.log("person recongnized");
    writeToScreen("Hi "+person+ ", We recommend this course"); //소리내기: 뫄뫄님 안녕하세요!!!!! //DB에서 꺼내오기
    doSend_ticket();

  }
  else if(work_type==2) //humidity
  {
    if (person=="open")
    {
      console.log("Dehumidification mode on");
      //소리내기 습도조절을 시작합니다!!!
    }
    else if (person=="close")
    {
      console.log("Dehumidification complete");
      //소리내기 습도조절이 완료되었습니다!
    }
    else
    {
      console.log("소리안냄");      
    }
    doSend_ticket(); 
  }
  else if (work_type==1 && username=="1")
  { //work_type ==1
    var message_send = {
      "work" : "1"
  };
    setTimeout(function() {
      websocket.send(JSON.stringify(message_send));
      console.log(stylingType_done + ' DONE')
    }, 5000);
  }
  else{

  }

}
function onError(evt)
{
  console.log('ERROR:'+ evt.data);
}
function doSend(stylingType)
{
  var message_send = {
    "work" : "1"
};
console.log(stylingType + ' START STYLING')
console.log("SENT: " + JSON.stringify(message_send));
//작업시작 메시지
websocket.send(JSON.stringify(message_send));
stylingType_done = stylingType;

}
function doSend_ticket()
{
  var message_send = {
      'work':'ticket'
  };
  console.log("SENT: " + JSON.stringify(message_send));
  websocket.send(JSON.stringify(message_send));
}
function writeToScreen(message)
{
   var greet = document.getElementById("ButtonUI");
   greet.innerHTML = message;
  //  output.appendChild(pre);
   console.log(message)
}
// Notification code will be put here
window.addEventListener("load", init, false);