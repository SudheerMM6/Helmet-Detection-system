const express = require("express");
const router = express.Router();
const path = require("path");

const dashboardUser = process.env.DASHBOARD_USER || "admin@example.com";
const dashboardPassword = process.env.DASHBOARD_PASSWORD || "change-me";

router.post('/login', (req, res)=>{
    if(req.body.email === dashboardUser && req.body.password === dashboardPassword){
        req.session.user = req.body.email;
        res.redirect('/route/dashboard');
    }else{
        res.status(401).render('base', {
            title: "Helmet Detection Dashboard",
            error: "Invalid email or password"
        });
    }
});

router.get('/dashboard', (req, res) => {
    if (req.session.user) {
        const filePath = path.join(__dirname, 'views/dashboard.html');
        res.sendFile(filePath);
    } else {
        res.status(401).render('base', {
            title: "Helmet Detection Dashboard",
            error: "Please log in to open the dashboard"
        });
    }
});

router.get('/logout', (req ,res)=>{
    req.session.destroy(function(err){
        if(err){
            res.status(500).send("Could not log out")
        }else{
            res.render('base', {
                title: "Helmet Detection Dashboard",
                logout : "Logged out successfully"
            })
        }
    })
})

module.exports = router;
