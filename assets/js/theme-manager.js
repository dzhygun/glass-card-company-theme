class ThemeManager {
    static #lightTheme = "light";
    static #darkTheme = "dark"

    static #root = document.documentElement;

    static buttonThemeSwitchIdDesktop = "theme-switch"
    static buttonThemeSwitchIdMobile = "theme-switch-mobile"
    static isThemeSwitchEnabled = window.appConfig.isThemeSwitchEnabled

    static initColorTheme() {
        const theme = ThemeManager.#getCurrentTheme()
        ThemeManager.#activateAndStoreTheme(theme)
    }
    static #getCurrentTheme() {
        if (ThemeManager.isThemeSwitchEnabled) {
            let storedTheme = localStorage.getItem("theme");
            if (storedTheme) {
                return storedTheme;
            }
        }

        let initialTheme = getComputedStyle(ThemeManager.#root).getPropertyValue('--predefined-theme').trim();
        if (initialTheme === 'auto') {
            return window.matchMedia(`(prefers-color-scheme: ${ThemeManager.#darkTheme})`).matches ? ThemeManager.#darkTheme : ThemeManager.#lightTheme
        }

        return initialTheme;
    }
    static #activateAndStoreTheme = (newTheme) => {
        ThemeManager.#root.dataset.theme = newTheme;
        localStorage.setItem("theme", newTheme);
        window.appConfig.themeButtonText = ThemeManager.#getButtonText(newTheme);
    }
    static #getButtonText = (newTheme) => {
        if (newTheme === ThemeManager.#darkTheme) {
            return window.appConfig.translations.themeSwitchValueDark;
        } else if (newTheme === ThemeManager.#lightTheme) {
            return window.appConfig.translations.themeSwitchValueLight;
        }
        throw new Error(`Unknown theme: ${newTheme}`);
    }
    static updateButtonText = (newTheme, buttonThemeSwitch) => {
        buttonThemeSwitch.textContent = this.#getButtonText(newTheme);
    }


    constructor(buttonThemeSwitchId) {
        this.buttonThemeSwitch = document.getElementById(buttonThemeSwitchId);
    }
    run() {
        const theme = ThemeManager.#getCurrentTheme()
        ThemeManager.updateButtonText(theme, this.buttonThemeSwitch)
        this.buttonThemeSwitch.addEventListener("click", () => {
            const theme = ThemeManager.#getCurrentTheme()
            const newTheme = theme === ThemeManager.#darkTheme ? ThemeManager.#lightTheme : ThemeManager.#darkTheme
            ThemeManager.#activateAndStoreTheme(newTheme, this.buttonThemeSwitch)
        })
    }
}

ThemeManager.initColorTheme();
document.addEventListener('DOMContentLoaded', () => {
    const themeManager = new ThemeManager(ThemeManager.buttonThemeSwitchIdDesktop);
    if (ThemeManager.isThemeSwitchEnabled) {
        themeManager.run();

    }
});