from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

app = Flask(__name__)


@app.route('/')
def home_page():
    # return "This is a home page of TechMap"
    return render_template('index.html')

@app.route('/skillset')
def skillset():
    return render_template('skillset.html')

@app.route('/result', methods=['POST','GET'])
def result():
    if request.method =='POST':
        skills = str(request.form['skills'])
        domain_knowledge = str(request.form['domain_knowledge'])
        interest = str(request.form['interest'])
        user_input = skills + ' ' + domain_knowledge + ' ' + interest
        user_input = user_input.replace(',',' ')
        user_domain = user_input.lower()
        dataset = pd.read_excel('AI Model Dataset.xlsx')
        dataset2 = pd.read_excel('Result.xlsx')
        dataset.loc[len(dataset.index)] = ['user_input', 'user', user_domain]
        # df = dataset
        # dataset = df.append(['user_input', 'user', user_domain], ignore_index=True)
        dataset["ids"]=[i for i in range(0,dataset.shape[0])]
        vectorizer= CountVectorizer() 
        cm= vectorizer.fit_transform(dataset['Keywords'])
        cs= cosine_similarity(cm)
        domain = 'user_input'
        domain_id = dataset[dataset.Domains == domain]['ids'].values[0]
        scores= list(enumerate(cs[domain_id]))
        sorted_scores= sorted(scores, key=lambda x:x[1],reverse=True)
        sorted_scores = sorted_scores[1:]
        j=0
        domain = 'user_input'
        recommendation = {}
        for score in sorted_scores:
            similar_domain = dataset[dataset.ids == score[0]]['Domains'].values[0]
            about = dataset2[dataset.ids == score[0]]['About'].values[0]
            recommendation[similar_domain] = about
            j=j+1
            if j>5:
                break
    return render_template('result.html', recommend = recommendation)



if __name__ == "__main__":
    app.run(debug=True)