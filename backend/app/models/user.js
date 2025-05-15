// /models/user.js
const db = require('../db');  

const User = db.define('user', {
    username: {
        type: db.Sequelize.STRING,
        allowNull: false,
        unique: true
    },
    email: {
        type: db.Sequelize.STRING,
        allowNull: false,
        unique: true
    },
    password_hash: {
        type: db.Sequelize.STRING,
        allowNull: false
    },
    created_at: {
        type: db.Sequelize.DATE,
        defaultValue: db.Sequelize.NOW
    }
});

module.exports = User;
