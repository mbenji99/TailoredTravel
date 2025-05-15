const colors = require('tailwindcss/colors')

module.exports = {
    purge: [],
    darkMode: false, // or 'media' or 'class'
    theme: {
        extend: {},
    },
    variants: {
        extend: {
            colors: {
                olive: {
                    200: '#b5b58d',
                },
            },
        },
    },
    plugins: [],
}