/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ['site/**/*.html', 'templates/**/*.html', 'pages/**/*.md'],
    theme: {
        extend: {
            screens: {
                print: { raw: 'print' },
            },
        },
    },
    plugins: [],
};
