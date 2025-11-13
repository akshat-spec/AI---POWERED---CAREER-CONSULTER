from flask import Flask, render_template, request, session, redirect, url_for
import pickle
import numpy as np

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a secure key

# Simple in-memory user storage (replace with database in production)
users = {}


@app.route('/')
def career():
    if 'loggedin' in session:
        return render_template("hometest.html")
    else:
        return redirect(url_for('signup'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return render_template("signup.html", error="Username already exists")
        users[username] = password
        session['loggedin'] = True
        session['username'] = username
        return redirect(url_for('career'))
    return render_template("signup.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['loggedin'] = True
            session['username'] = username
            return redirect(url_for('career'))
        else:
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/blog')
def blog():
    return render_template("blog.html")

@app.route('/courses')
def courses():
    return render_template("courses.html")

@app.route('/predict',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      i = 0
      print(result)
      res = result.to_dict(flat=True)
      print("res:",res)
      arr1 = res.values()
      arr = ([int(value) for value in arr1])

      data = np.array(arr)

      data = data.reshape(1,-1)
      print(data)
      loaded_model = pickle.load(open("careerlast.pkl", 'rb'))
      predictions = loaded_model.predict(data)
     # return render_template('testafter.html',a=predictions)

      print(predictions)
      pred = loaded_model.predict_proba(data)
      print(pred)
      #acc=accuracy_score(pred,)
      pred = pred > 0.05
      #print(predictions)
      i = 0
      j = 0
      index = 0
      res = {}
      final_res = {}
      while j < 17:
          if pred[i, j]:
              res[index] = j
              index += 1
          j += 1
      # print(j)
      #print(res)
      index = 0
      for key, values in res.items():
          if values != predictions[0]:
              final_res[index] = values
              print('final_res[index]:',final_res[index])
              index += 1
      #print(final_res)
      jobs_dict = {0:'AI ML Specialist',
                   1:'API Integration Specialist',
                   2:'Application Support Engineer',
                   3:'Business Analyst',
                   4:'Customer Service Executive',
                   5:'Cyber Security Specialist',
                   6:'Data Scientist',
                   7:'Database Administrator',
                   8:'Graphics Designer',
                   9:'Hardware Engineer',
                   10:'Helpdesk Engineer',
                   11:'Information Security Specialist',
                   12:'Networking Engineer',
                   13:'Project Manager',
                   14:'Software Developer',
                   15:'Software Tester',
                   16:'Technical Writer'}

      php_dict = {0: 'AI_ML_Specialist.php',
                  1: 'API_Integration _Specialist.php',
                  2: 'Application_Support_Engineer.php',
                  3: 'Business_Analyst.php',
                  4: 'Customer_service_executive.php',
                  5: 'Cyber_Security_Specialist.php',
                  6: 'Data_Scientist.php',
                  7: 'Database_Administrator.php',
                  8: 'Graphic_Designer.php',
                  9: 'Hardware_Engineer.php',
                  10: 'Helpdesk_Engineer.php',
                  11: 'Information_security.php',
                  12: 'Networking_engineer.php',
                  13: 'Project_Manager.php',
                  14: 'Software_developer.php',
                  15: 'Software_tester.php',
                  16: 'Technical_writer.php'}

      #print(jobs_dict[predictions[0]])
      job = {}
      #job[0] = jobs_dict[predictions[0]]
      index = 1


      data1=predictions[0]
      print(data1)
      return render_template("testafter.html",final_res=final_res,job_dict=jobs_dict,job0=data1,php_dict=php_dict)
      
if __name__ == '__main__':
   app.run(debug = True)
