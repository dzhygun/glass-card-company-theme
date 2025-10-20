// ✅ CommonJS, not ESM
const fs = require('fs');
const path = require('path');

module.exports = function (Handlebars) {
    return {
        svg: function (relPath) {
try {
      // Resolve relative to the theme root
      const themeRoot = path.join(__dirname);            // helpers.js is in theme root
      const absPath   = path.join(themeRoot, relPath);

      const contents = fs.readFileSync(absPath, 'utf8');
      return new Handlebars.SafeString(contents);
    } catch (err) {
      console.error('[inline helper] Failed to read', relPath, err);
      return ''; // don’t break rendering
    }
        }

    }
};
