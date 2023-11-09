/** @type {import('tailwindcss').Config} */
const defaultTheme = require('tailwindcss/defaultTheme');

module.exports = {
    content: ['site/**/*.html', 'templates/**/*.html', 'pages/**/*.md'],
    theme: {
        fontFamily: {
            sans: ["'Mona Sans'", ...defaultTheme.fontFamily.sans],
            headline: ["'Hubot Sans'", ...defaultTheme.fontFamily.sans],
        },
        extend: {
            screens: {
                print: { raw: 'print' },
            },
        },
    },
    plugins: [],
};
