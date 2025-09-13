# README
If overriden theme overrides `assets/js/scripts.js`, then `scripts.min.js` needs to be regenerated manually.

Execute following:

```bash
cp ./minify_scripts.sh ../../../card-glass-company-theme-override/assets/js/scripts/
cd ../../../card-glass-company-theme-override/assets/js/scripts/
./minify_scripts.sh
```

Afterwards, you can just run the `minify_scripts.sh` directly from the `card-glass-company-theme-override/assets/js/scripts/`