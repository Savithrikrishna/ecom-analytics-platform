function saveGmailAttachmentToGCS() {
  var bucketName = "poc-csv-data-source";
  var query = "from:<source-email> has:attachment filename:daily_orders";
  
  // 1. Search for the email
  var threads = GmailApp.search(query, 0, 1);
  if (threads.length == 0) return;
  
  var messages = threads[0].getMessages();
  var lastMessage = messages[messages.length - 1];
  var attachments = lastMessage.getAttachments();
  
  for (var i = 0; i < attachments.length; i++) {
    var attachment = attachments[i];
    if (attachment.getContentType() === "text/csv") {
      
      // 2. Upload to GCS using Google's API
      var url = "https://storage.googleapis.com/upload/storage/v1/b/" + bucketName + "/o?uploadType=media&name=" + attachment.getName();
      var response = UrlFetchApp.fetch(url, {
        method: "POST",
        headers: {
          Authorization: "Bearer " + ScriptApp.getOAuthToken()
        },
        payload: attachment.copyBlob(),
        contentType: "text/csv"
      });
      
      Logger.log("Uploaded: " + attachment.getName());
    }
  }
}
