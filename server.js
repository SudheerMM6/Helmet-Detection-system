const express = require('express');
const path = require('path');
const crypto = require('crypto');
const session = require("express-session");
require('dotenv').config();

const router = require('./router');

const app = express();

const port = process.env.PORT || 3000;
const isProduction = process.env.NODE_ENV === 'production';

function getSessionSecret() {
    if (process.env.SESSION_SECRET) {
        return process.env.SESSION_SECRET;
    }

    if (isProduction) {
        throw new Error('SESSION_SECRET is required when NODE_ENV=production');
    }

    console.warn('SESSION_SECRET is not set. Using a temporary local-only session secret.');
    return crypto.randomBytes(32).toString('hex');
}

const sessionSecret = getSessionSecret();

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.set('view engine', 'ejs');

// load static assets
app.use('/static', express.static(path.join(__dirname, 'public')));
app.use('/assets', express.static(path.join(__dirname, 'public/assets')));

app.use(session({
    secret: sessionSecret,
    resave: false,
    saveUninitialized: false
}));

app.use('/route', router);

app.get('/', (req, res) => {
    res.render('base', { title: "Helmet Detection Dashboard" });
});

app.listen(port, () => {
    console.log(`Helmet dashboard running on http://localhost:${port}`);
});
