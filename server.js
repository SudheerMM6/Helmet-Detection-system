const express = require('express');
const path = require('path');
const crypto = require('crypto');
const session = require("express-session");

const router = require('./router');

const app = express();

const port = process.env.PORT || 3000;
const sessionSecret = process.env.SESSION_SECRET || crypto.randomBytes(32).toString('hex');

app.use(express.json());
app.use(express.urlencoded({ extended: true }))

app.set('view engine', 'ejs');

// load static assets
app.use('/static', express.static(path.join(__dirname, 'public')))
app.use('/assets', express.static(path.join(__dirname, 'public/assets')))

app.use(session({
    secret: sessionSecret,
    resave: false,
    saveUninitialized: false
}));

app.use('/route', router);

app.get('/', (req, res) =>{
    res.render('base', { title : "Helmet Detection Dashboard"});
})

app.listen(port, () => {
    console.log(`Helmet dashboard running on http://localhost:${port}`);
});
