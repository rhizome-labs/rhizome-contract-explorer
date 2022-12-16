const colors = require('tailwindcss/colors')

module.exports = {
  content: ["./rhizome_contract_explorer/app/templates/**/*.{html,js}"],
  theme: {
    colors: {
      transparent: 'transparent',
      current: 'currentColor',
      black: colors.black,
      cyan: colors.cyan,
      white: colors.white,
      gray: colors.slate,
      green: colors.emerald,
      orange: colors.orange,
      purple: colors.purple,
      red: colors.red,
      yellow: colors.yellow
    },
    extend: {}
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}
