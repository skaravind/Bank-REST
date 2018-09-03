from bottle import run, get, post, request, error
import pandas as pd
import os

df = pd.read_csv("bank_branches.csv")


@get('/ifsc_lookup/<ifsc>')
def ifsc_lookup(ifsc):
	result = df.loc[df['ifsc'] == ifsc]
	if len(result) == 0:
		return {'Error':'Bank with the given ifsc does not exist'}
	else:
		data = {
		"bank_id" : str(result['bank_id'].values[0]),
		"branch" : result['branch'].values[0],
		"address" : result['address'].values[0],
		"city" : result["city"].values[0],
		"district" : result["district"].values[0],
		"state" : result['state'].values[0],
		"bank_name" : result['bank_name'].values[0]
		}
		return data


@post('/bank_city_lookup')
def bank_city():
	if request.json != None:
		results = df.loc[(df['bank_name'] == request.json.get('bank_name').upper()) & (df['city'] == request.json.get('city').upper())]
		if len(results) == 0:
			return {'Error':'No bank found from the given details'}
		else:
			final = {"Matches" : []}
			for result in results.values:
				data = {
				"ifsc" : str(result[0]),
				"bank_id" : str(result[1]),
				"branch" : result[2],
				"address" : result[3],
				"city" : result[4],
				"district" : result[5],
				"state" : result[6],
				"bank_name" : result[7]
				}
				final["Matches"].append(data)
			
			return final


@error(404)
def error404(error):
    return {'error' : '404 error. Nothing to see here'}


run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

#run(host='localhost', port=8080, debug=True)


#h = df.loc[(df['bank_name'] == "ABHYUDAYA COOPERATIVE BANK LIMITED") & (df['city'] == "MUMBAI")]

