from flask import Flask, request, jsonify

app = Flask(__name__)

html_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Flask Calculator</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
      background-color: #f0f2f5;
    }
    .calculator {
      background: #fff;
      padding: 20px;
      border-radius: 12px;
      box-shadow: 0 8px 20px rgba(0,0,0,0.1);
      max-width: 320px;
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 10px;
    }
    input[type="text"] {
      grid-column: span 4;
      height: 60px;
      text-align: right;
      font-size: 24px;
      margin-bottom: 10px;
      border: none;
      background-color: #e8f0fe;
      border-radius: 8px;
      padding: 10px;
    }
    button {
      height: 60px;
      font-size: 18px;
      background-color: #007bff;
      color: white;
      border: none;
      border-radius: 8px;
      cursor: pointer;
    }
    button.operator { background-color: #ff5722; }
    button.double { grid-column: span 2; }
    button:active { opacity: 0.8; }
  </style>
</head>
<body>
  <div class="calculator">
    <input type="text" id="display" disabled />
    <button class="double" onclick="clearDisplay()">C</button>
    <button onclick="appendValue('(')">(</button>
    <button onclick="appendValue(')')">)</button>
    <button class="operator" onclick="appendValue('/')">÷</button>
    <button onclick="appendValue('7')">7</button>
    <button onclick="appendValue('8')">8</button>
    <button onclick="appendValue('9')">9</button>
    <button class="operator" onclick="appendValue('*')">×</button>
    <button onclick="appendValue('4')">4</button>
    <button onclick="appendValue('5')">5</button>
    <button onclick="appendValue('6')">6</button>
    <button class="operator" onclick="appendValue('-')">-</button>
    <button onclick="appendValue('1')">1</button>
    <button onclick="appendValue('2')">2</button>
    <button onclick="appendValue('3')">3</button>
    <button class="operator" onclick="appendValue('+')">+</button>
    <button class="double" onclick="appendValue('0')">0</button>
    <button onclick="appendValue('.')">.</button>
    <button class="operator" onclick="calculate()">=</button>
  </div>

  <script>
    function appendValue(value) {
      document.getElementById('display').value += value;
    }

    function clearDisplay() {
      document.getElementById('display').value = '';
    }

    function calculate() {
      const display = document.getElementById('display');
      fetch('/calculate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ expression: display.value })
      })
      .then(response => response.json())
      .then(data => {
        if (data.error) {
          display.value = 'Error';
        } else {
          display.value = data.result;
        }
      });
    }
  </script>
</body>
</html>
'''

@app.route('/')
def index():
    return html_content

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.json
        expression = data.get('expression', '')
        result = str(eval(expression))
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
