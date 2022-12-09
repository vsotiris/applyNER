from flask import Flask, render_template, request
import pandas as pd
import nerfunctions as ner



app = Flask(__name__, template_folder="templates")


timeperiod='1m'

@app.route("/", methods=["GET","POST"])
def home():
    if request.method=="POST":
        print('*** in post')
        keywords = request.form['keywords']
        print(keywords)
        out = ner.find_entities(keywords, timeperiod)
        print(out)
        df = pd.DataFrame(out)
        df.columns = ['Entity', 'Freq']
        dfout=df
        #dfout = df.set_index('Entity')
        print(dfout.head(10))

        return render_template("index.html",
                               row_data=list(dfout.values.tolist()),
                               column_names=dfout.columns.values,
                               zip=zip)
    else:
        #return render_template("index.html",
        #                       row_data="",
        #                       column_names="",
        #                       zip=zip)

        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)