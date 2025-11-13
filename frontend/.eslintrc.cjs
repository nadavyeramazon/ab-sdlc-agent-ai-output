module.exports = {
  root: true,
  env: { browser: true, es2020: true },
  extends: [
    'eslint:recommended',
    'plugin:react/recommended',
    'plugin:react/jsx-runtime',
    'plugin:react-hooks/recommended',
  ],
  ignorePatterns: ['dist', '.eslintrc.cjs'],
  parserOptions: { ecmaVersion: 'latest', sourceType: 'module' },
  settings: { react: { version: '18.2' } },
  plugins: ['react-refresh'],
  rules: {
    'react-refresh/only-export-components': [
      'warn',
      { allowConstantExport: true },
    ],
    'react/prop-types': 'off',
  },
  overrides: [
    {
      // Test files configuration
      files: ['**/*.test.js', '**/*.test.jsx', '**/*.spec.js', '**/*.spec.jsx', '**/setupTests.js'],
      env: {
        browser: true,
        es2020: true,
        node: true, // Enable Node.js globals like 'global' for test files
      },
    },
    {
      // Config files run in Node.js environment
      files: ['vite.config.js', '*.config.js'],
      env: {
        node: true, // Enable Node.js globals like 'process' for config files
        es2020: true,
      },
    },
  ],
}
