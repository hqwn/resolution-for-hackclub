from browser import document, html, window, aio
import json

local_storage = window.localStorage
async def register_user_async():

    name = document["name"].value

    if not name:
        window.alert("Please enter a name!")
        return

    req = await aio.post("/register", headers={"Content-Type": "application/json"}, data=json.dumps({"name": name}))
    if req.status == 200:

        data = json.loads(req.data)
        local_storage.setItem("api_key", data["api_key"])
        window.alert(f"Registration successful! Your API key has been saved to local storage. It is {data['api_key']}. Will only show this once, so make sure to save it somewhere safe!")
        
        div = document["app"]
        div.clear()
        routes()

async def get_quote_async():
    req = await aio.get("/quote", headers={"x-api-key": local_storage['api_key']})

    if req.status == 200:
        data = json.loads(req.data)
        document["text"].text = f'"{data['quote']}" by {data['owner'].capitalize()}'
    if req.status == 429:
        document["text"].text = 'To many requests!'

async def add_quote_async():
    quote_text = document["quote"].value

    if not quote_text:
        window.alert('Please enter a quote!')
        return

    req = await aio.post("/quote", headers={"x-api-key": local_storage['api_key'], "Content-Type": "application/json"}, data = json.dumps({"new_quote": quote_text}))

    if req.status == 200:
        document["text"].text = f'Quote, "{quote_text}" added!'
        document["quote"].value = ""
        return
    else:
        document['text'].text = f'Error {req.status} occured'
        return

async def delete_async():
    req = await aio.ajax("DELETE", "/quotes/delete", headers={"x-api-key": local_storage['api_key']})

    if req.status == 200:
        document["text"].text = 'All of your quotes are deleted!'
        return
    else:
        document['text'].text = f'Error {req.status} occured'
        return


def get_a_quote(event):
    aio.run(get_quote_async())

def add_a_quote(event):
    aio.run(add_quote_async())

def delete_quotes(event):
    aio.run(delete_async())

def register_user(event):
    aio.run(register_user_async())

def login_user(event):
    key = document["name"].value
    local_storage.setItem("api_key", key)
    window.alert("API key saved to local storage!")
    div = document["app"]
    div.clear()
    routes()

def routes():
    div = document["app"]

    section = html.DIV(id = 'section')
    section2 = html.DIV(id = 'section2')

    get_quote = html.BUTTON("Get Quote", id="get_quote")
    quote = html.INPUT(type="text", placeholder="Quote", id="quote")
    add_quote = html.BUTTON("Add Quote", id="add_quote")
    delete_btn = html.BUTTON("Delete all of your quotes", id="delete")
    text = html.H3("Your Request's output goes here!", id='text')
    
    get_quote.bind("click", get_a_quote)
    add_quote.bind("click", add_a_quote)
    delete_btn.bind("click", delete_quotes)

    section.appendChild(quote)
    section.appendChild(add_quote)
    section2.append(text)

    div.appendChild(section2)
    div.appendChild(get_quote)
    div.appendChild(section)
    div.appendChild(delete_btn)
    # div.appendChild(div2)
    # div.appendChild(add_quote)
    

def register():
    div = document["app"]

    name = html.INPUT(type="text", placeholder="Name/API Key (name to register, API key to log in)", id="name")
    submit = html.BUTTON("Register", id="submit")
    login = html.BUTTON("Log IN", id="login")
    submit.bind("click", register_user)
    login.bind("click", login_user)

    div.appendChild(name)
    div.appendChild(html.BR())
    div.appendChild(submit)
    div.appendChild(login)

#Detecing if API key exists in local storage, if not, show registration page, else show routes
