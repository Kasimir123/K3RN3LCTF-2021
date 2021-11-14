const express = require('express')
const sqlite3 = require('sqlite3').verbose()

const app = express()
const db = new sqlite3.Database('database.db')

const flag = "ictf{flag}"

db.run('CREATE TABLE users (id INTEGER PRIMARY KEY, token TEXT, money INTEGER, pity INTEGER)', err => {
    if (!err) {
        console.log("Initializing database")
        db.serialize(() => {
            db.run('CREATE TABLE characters (id INTEGER PRIMARY KEY, name TEXT, rarity REAL, description TEXT)')
            let stmt = db.prepare('INSERT INTO characters (name, rarity, description) VALUES (?, ?, ?)')
            stmt.run("ainz", 0.000000000000001, "Formerly known as Momonga, Ainz is regarded as the highest of the Almighty Forty-One Supreme Beings by the NPCs of Nazarick. <br>" + flag)
            stmt.run("albedo", 0.15, "The Overseer of the Guardians of the Great Tomb of Nazarick")
            stmt.run("demiurgus", 0.15, "The Floor Guardian of the 7th Floor of the Great Tomb of Nazarick and the Commander of the NPC defenses.")
            stmt.run("sebas", 0.15, "The head butler of the Great Tomb of Nazarick. He is also the leader of the Pleiades Six Stars.")
            stmt.run("cocytus", 0.15, "The Floor Guardian of the 5th Floor in the Great Tomb of Nazarick.")
            stmt.run("shalltear", 0.15, "A true vampire and the Floor Guardian of the first to third floors in the Great Tomb of Nazarick.")
            stmt.run("mare", 0.125, "A dark elf and one of the twin Floor Guardians on the 6th Floor of the Great Tomb of Nazarick.")
            stmt.run("aura", 0.125, "A dark elf and one of the twin Floor Guardians on the 6th Floor in the Great Tomb of Nazarick.")
            stmt.finalize()
        })
    } else { console.log("Skipping database initialization") }
})

function generateToken() {
    let result = "";
    for (var i = 0; i < 10; i++) {
        append = Math.floor(Math.random() * (2**32)).toString(16)
        while (append.length < 8) { append = "0" + append }
		result += append
    }
    return result;
}

app.get('/start', (req, res) => {
    let token = generateToken()
    db.run("INSERT INTO users (token, money, pity) VALUES (?, ?, ?)", token, 100, 0, err => {
        if (err) {
            res.json({ "success": false })
            return
        }
        res.json({ "success": true, "data": token })
    })
})

app.get('/user', (req, res) => {
    let token = req.query.token;
    db.get("SELECT * FROM users WHERE token = ?", token, (err, row) => {
        if (err || !row) {
            res.json({ "success": false })
            return
        }
        res.json({ "success": true, "data": row })
    })
})

app.get('/leaderboard', (req, res) => {
    db.all("SELECT * FROM users ORDER BY pity DESC LIMIT 4", (err, rows) => {
        if (err || !rows) {
            res.json({ "success": false })
            return
        }
        rows.forEach(row => {
            row.token = row.token.substring(0, 48) + "*".repeat(32)
        })
        res.json({ "success": true, "data": rows })
    })
})

app.get('/earn', (req, res) => {
    let token = req.query.token;
    db.get("SELECT * FROM users WHERE token = ?", token, (err, row) => {
        if (err || !row) {
            res.json({ "success": false })
            return
        }
        db.run("UPDATE users SET money = money + 10 WHERE token = ?", token, err => {
            if (err) {
                res.json({ "success": false })
            }
            res.json({ "success": true })
        })
    })
})

app.get('/pull', (req, res) => {
    let token = req.query.token;
    db.get("SELECT * FROM users WHERE token = ?", token, (err, row) => {
        if (err || !row || row.money < 10) {
            res.json({ "success": false })
            return
        }
        let rand = Math.random()
        let sum = 0
        let guaranteed = row.pity >= 999999999999
        db.all("SELECT * FROM characters ORDER BY id ASC", (err, rows) => {
            if (err) {
                res.json({ "success": false })
                return
            }
            rows.some(row => {
                sum += row.rarity
                if (rand < sum && !guaranteed) {
                    res.json({ "success": true, "data": row })
                    return true
                }
                if (guaranteed && row.name == "ainz") {
                    res.json({ "success": true, "data": row })
                    return true
                }
            })
            db.run("UPDATE users SET money = money - 10, pity = pity + 1 WHERE token = ?", token);
        })
    })
})

app.listen(3000, () => {
    console.log("Server listening at http://localhost:3000")
})