server_url = "http://206.81.1.65:3000";

window.onload = () => {
    document.getElementById("op1").play()

    let characters = ["ainz", "albedo", "demiurgus", "sebas", "cocytus", "shalltear", "mare", "aura"]
    characters.forEach(char => {
        if (!localStorage.getItem(char)) localStorage.setItem(char, 0)
    })

    let token = localStorage.getItem("token")
    if (!token) {
        fetch(server_url + "/start").then(response => response.json()).then(json => {
            if (json.success === true) {
                localStorage.setItem("token", json.data)
                updateMoney()
            }
        })
    } else {
        updateMoney()
    }
}

function updateMoney() {
    let token = localStorage.getItem("token")
    fetch(server_url + "/user?token=" + token).then(response => response.json()).then(json => {
        if (json.success === true) {
            document.getElementById("coins").innerText = json.data.money
        }
    })
}

function pullCharacter() {
    let token = localStorage.getItem("token")
    fetch(server_url + "/pull?token=" + token).then(response => response.json()).then(json => {
        if (json.success === true) {
            document.getElementById("pull-title").innerText = "You got " + json.data.name
            document.getElementById("character-image").src = `assets/characters/${json.data.name}.png`
            document.getElementById("character-description").innerHTML = json.data.description
            new bootstrap.Modal(document.getElementById("pull")).show()
            localStorage.setItem(json.data.name, parseInt(localStorage.getItem(json.data.name)) + 1)
            updateMoney()
        } else {
            earnCoins()
        }
    })
}

function earnCoins() {
    let ad = new bootstrap.Modal(document.getElementById("ad"))
    ad.show()
    document.getElementById("op1").pause()
    document.getElementById("ad-video").play()
    window.setTimeout(() => {
        ad.hide()
        document.getElementById("op1").play()
        let token = localStorage.getItem("token")
        fetch(server_url + "/earn?token=" + token).then(updateMoney())
    }, 10500)
}

function viewCharacters() {
    let charactersContainer = document.getElementById("characters-container")
    charactersContainer.innerHTML = "";
    let characters = ["albedo", "ainz", "demiurgus", "sebas", "cocytus", "shalltear", "mare", "aura"]
    characters.forEach(char => {
        let element = document.createElement("div")
        element.classList.add("col-4")
        element.classList.add("mb-5")
        if (char === "ainz") element.classList.add("text-danger")
        element.innerText = char.charAt(0).toUpperCase() + char.slice(1) + " x " + localStorage.getItem(char)
        charactersContainer.appendChild(element)
    })
    new bootstrap.Modal(document.getElementById("characters")).show()
}

function viewLeaderboard() { 
    let leaderboardContainer = document.getElementById("leaderboard-container")
    leaderboardContainer.innerHTML = "";
    let token = localStorage.getItem("token")
    fetch(server_url + "/leaderboard?token=" + token).then(response => response.json()).then(json => {
        if (json.success === true) {
            json.data.forEach(user => {
                let tokenElement = document.createElement("p")
                tokenElement.classList.add("token")
                tokenElement.classList.add("my-2")
                tokenElement.innerText = `${user.token.substring(0,32)}(...) - ${user.pity} pulls`
                leaderboardContainer.appendChild(tokenElement)
            })
        }
    })
    new bootstrap.Modal(document.getElementById("leaderboard")).show()
}

function showFirstPage() {
    let navigationButton = document.getElementById("navigation-button")
    let firstPage = document.getElementById("first-page")
    let secondPage = document.getElementById("second-page")
    navigationButton.innerText = "NEXT PAGE >>"
    firstPage.classList.remove("d-none")
    secondPage.classList.add("d-none")
    new bootstrap.Modal(document.getElementById("information")).show()
}

function changePage() {
    let navigationButton = document.getElementById("navigation-button")
    let firstPage = document.getElementById("first-page")
    let secondPage = document.getElementById("second-page")
    if (firstPage.classList.contains("d-none")) {
        navigationButton.innerText = "NEXT PAGE >>"
        firstPage.classList.remove("d-none")
        secondPage.classList.add("d-none")
    } else {
        navigationButton.innerText = "<< PREVIOUS PAGE"
        firstPage.classList.add("d-none")
        secondPage.classList.remove("d-none")
    }
}