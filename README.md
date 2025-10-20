# Glass Card Company Theme - for Publii
<img width="2560" height="1440" alt="image" src="https://github.com/user-attachments/assets/ea924031-f24e-4031-af25-4af36c9f2148" />

The theme is intended to be used for "visit-card" websites by private individuals or companies.
Therefore the theme is cleaned up from all unnecessary features, like posts, tags, search etc.

## Preview

- Master branch: https://publii-glass-card-company-theme.zolotukhin.ch/
- Development branch: https://development-publii-glass-card-company-theme.zolotukhin.ch/
  - Authorization: all emails are valid.

## Supported features
- Pages
- Light/Dark theme toggle
- Mobile view
- Unlike other themes and contrary to Publii documentation, the theme works without posts.

## Installation
- Import the `glass-card-company-theme.zip` as per docs: https://getpublii.com/docs/installing-using-updating-themes.html
- Default favicon, logo and background images are located in the theme root directory. Set them manually through Publii interface, if needed.

### KNOWN BUGS
- Disable Site settings/Website speed/CSS compression. It deletes `.css` files.

## Credits
- This theme is based on [Publii Simple Theme v.3.1.3.0](https://marketplace.getpublii.com/themes/simple/).
- Default background photo `default_bg.jpg` by <a href="https://unsplash.com/@purzlbaum?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash">Claudio Schwarz</a> on <a href="https://unsplash.com/photos/a-red-bench-sitting-in-the-middle-of-a-courtyard-J_jSmZUakwI?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash">Unsplash</a>
    
## TODO
- Missing css implementation to limit animations, transparency etc
- Missing cross-browser css implementation
- iOS 26 Safari - background is not extended to bottom and top limits (below floating browser elements)
- Add fade-in disable/duration control
- Make german translations
- Figure out why .svg are duplicated in .js and .svg file