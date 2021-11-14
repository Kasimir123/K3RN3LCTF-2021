#!/usr/local/bin/python
#
# Polymero
#

# Imports
from flask import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os, time, json, hmac, hashlib


class Cwypto:
	def __init__(self):
		self.key = os.urandom(16) # Encryption Key
		self.mak = os.urandom(16) # Message Authentication Key
		self.iv  = os.urandom(16) # Initial IV

	def encrypt(self, msg):
		# Encrypt
		pdm = pad(msg, 16)
		aes = AES.new(key=self.key, mode=AES.MODE_CBC, iv=self.iv)
		cip = self.iv + aes.encrypt(pdm)
		# Authenticate
		tag = hmac.new(self.mak, msg, hashlib.sha256).digest()[:16]
		# Update IV
		self.iv = cip[-16:]
		return cip + tag

	def decrypt(self, cip):
		# Decrypt
		iv, cip, tag = cip[:16], cip[16:-16], cip[-16:]
		aes = AES.new(key=self.key, mode=AES.MODE_CBC, iv=iv)
		pdm = aes.decrypt(cip)
		msg = unpad(pdm, 16)
		# Authenticate
		if hmac.new(self.mak, msg, hashlib.sha256).digest()[:16] == tag:
			return msg
		else:
			raise ValueError()

class Vault:
	def __init__(self):
		self.crypto = Cwypto()
		self.secret_combination = int.from_bytes(os.urandom(16),'big')

		with open('flag.txt','rb') as f:
			self.contents = f.read().decode()
			f.close()

	def access(self, token):
		try:
			token = self.crypto.decrypt(bytes.fromhex(token))
		except:
			return 1, 'Invalid decryption or authentication.'
		try:
			token = json.loads(token)
		except:
			return 1, 'Invalid JSON format.'
		try:
			b1 = token["user"] == "admin"
			b2 = "Vault.access()" in token["priv"]
			b3 = token["code"] == str(self.secret_combination)
			if all([b1, b2, b3]):
				return 0, None
			else:
				return 1, 'You do not have the required permissions.'
		except:
			return 1, 'Missing JSON components.'

	def create_token(self, user):
		token = {
			"user" : user,
			"iat"  : int(time.time()),
			"priv" : [],
			"code" : str(self.secret_combination)
		}
		token = self.crypto.encrypt(json.dumps(token).encode())
		return token.hex()

app   = Flask(__name__)
vault = Vault()
print(vault.secret_combination)



#------------------------------------------------------------------------------------------
# WEBPAGES
#------------------------------------------------------------------------------------------
@app.route('/', methods=['GET'])
def index():
	try:
		acto = request.cookies.get('access_token')
		if acto is None: raise ValueError()
		try:
			err, resp = vault.access(acto)
			if err:
				return render_template('invalid.html', error=resp)
			else:
				# Good luck, you'll need it!
				return render_template('flag.html', flag=vault.contents)
		except:
			return render_template('broken.html')
	except:
		return render_template('missing.html')

@app.route("/register/", methods=['GET'])
def register():
	return render_template('register.html')

# Necessary backwards compatibility
@app.route("/manual_override/", methods=['GET'])
def manual_override():
	return render_template('manual_override.html', dig=len(str(vault.secret_combination)))



#------------------------------------------------------------------------------------------
# APIs
#------------------------------------------------------------------------------------------
@app.route("/register_user/", methods=['POST'])
def register_user():
	user = request.form['user']
	acto = vault.create_token(user)
	resp = make_response(redirect('/'))
	resp.set_cookie('access_token', acto)
	return resp

@app.route("/override/", methods=['POST'])
def override():
	code = request.form['code']
	if code == str(vault.secret_combination):
		return render_template('flag.html', flag=vault.contents)
	return redirect('/')

# FOR DEVELOPERS ONLY, DELETE BEFORE DEPLOYMENT!
@app.route("/debug/", methods=['POST'])
def debug():
	msg = pad(bytes.fromhex(request.form['hex']), 16)
	aes = AES.new(key=vault.crypto.key, mode=AES.MODE_CBC, iv=b'4DEVELOPERSONLY!')
	cip = aes.encrypt(msg)
	return cip.hex()
		


if __name__ == '__main__':
	app.run()
