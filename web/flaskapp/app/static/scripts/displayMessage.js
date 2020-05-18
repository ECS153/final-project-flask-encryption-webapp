var currentlyDisplayedMessage = "placeholder"; // id of current display

function DisplayMessage(msgId)
{
  document.getElementById(currentlyDisplayedMessage).style.display="none";
  document.getElementById(msgId).style.display='inline';
  currentlyDisplayedMessage = msgId;
  window.scrollTo(0,document.body.scrollHeight);
  return;
}
