
# In[13]:
from flask import Flask,request,render_template
import pymysql as pml
import pandas as pd
import pickle as pkl

# In[14]:

log = pkl.load(open('reg.pkl','rb'))

# In[15]:

conn = pml.connect(user = 'root',host='localhost',port=3306,password='Raashid123',database='login')

# In[16]:

df = pd.read_sql(sql='select * from user',con=conn)

# In[17]:
    
app = Flask(__name__)

# In[18]:
    
@app.route("/")
def main():
    return render_template("index.html")


#%%

@app.route("/verify",methods=['POST'])
def verify():
    user = request.form.get('username')
    password = request.form.get('password') 
 
    if user in list(df['username']):
        
        row = df[df['username'] == user]
        
        if password in list(row['password']):
            return render_template('code.html')
        else:
            return render_template('index.html',result='invalid password or username')
    
    else:
        return render_template('index.html',result='invalid password or username')
    
#%%
@app.route("/path",methods=['POST'])
def pred():
    
    battery = int(request.form.get('battery'))
    clk = int(request.form.get('clk'))
    sim = int(request.form.get('sim'))
    fourg = int(request.form.get('4g'))
    mm = int(request.form.get('memory'))
    wt = int(request.form.get('wt'))
    cores = int(request.form.get('cores'))
    height = int(request.form.get('height'))
    width = int(request.form.get('width'))
    ram = int(request.form.get('ram'))
    threeg = int(request.form.get('3g'))
    touch = int(request.form.get('touch'))
    wifi = int(request.form.get('wifi'))
    
    op = log.predict([[battery,clk,sim,fourg,mm,wt,cores,height,width,ram,threeg,touch,wifi]])

    
    return render_template('result.html', val="The estimated value is {}".format(op[0]))
    
#%%
if __name__=='__main__':
    app.run(host='localhost',port=5000)
